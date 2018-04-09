"""
Given DUO and Schoolwijzer data, extract number of students and personel.
"""
# flake8: noqa
import logging
import pandas
from requests.exceptions import HTTPError

from django.db.models import Sum
from dataset.models import Vestiging, LeerlingLeraarRatio

_DATA_SET_URL = 'https://duo.nl/open_onderwijsdata/images/01-po-personen-owtype-bestuur-brin-functie.csv'

_N_PERSONEN_COLUMNS = {
    2011: "PERSONEN 2011",
    2012: "PERSONEN 2012",
    2013: "PERSONEN 2013",
    2014: "PERSONEN 2014",
    2015: "PERSONEN 2015",
    2016: "PERSONEN 2016",
}
_TARGET_FUNCTIEGROEP_ATTR = {
    'Directie': 'n_directie',
    'Onderwijsgevend personeel': 'n_onderwijzend',
    'Onderwijsondersteunend personeel (OOP/OBP)': 'n_ondersteunend',
    'Leraren in opleiding (LIO)': 'n_inopleiding',
    'Onbekend': 'n_onbekend'
}


LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def strip_column_names(df):
    df.rename(columns=lambda x: x.strip(), inplace=True)
    return df


def get_leerling_leraar_ratios(years):
    """
    Calculate the Leerling / Leraar ratio on per BRIN basis (not vestiging).
    """
    relevant_brins = Vestiging.objects.values_list('brin', flat=True).distinct()

    # Download and parse the relevant data:
    try:
        duo_data = pandas.read_csv(_DATA_SET_URL, delimiter=';', decimal=',')
    except:
        logger.error('Problem accessing: %s', _DATA_SET_URL)
        raise

    strip_column_names(duo_data)
    duo_data = duo_data[duo_data['BRIN NUMMER'].isin(relevant_brins)]

    # Sanity checks, log obvious problems.
    brin_nummers_duo = set(duo_data['BRIN NUMMER'])
    alleen_amsterdam = set(relevant_brins) - brin_nummers_duo
    alleen_duo = brin_nummers_duo - set(relevant_brins)
    logger.info('BRIN nummers aleen in Amsterdamse data: {}'.format(
        alleen_amsterdam))
    logger.info('Aantal BRIN nummers in Amsterdamse data: {}'.format(
        len(relevant_brins)))
    logger.info('BRIN nummers alleen in DUO data: {}'.format(alleen_duo))
    logger.info('Aantal BRIN nummers in DUO data: {}'.format(
        len(duo_data['BRIN NUMMER'].unique())))

    # Map BRIN to total number of students (because several vestigingen per BRIN).
    brin_leerlingen = dict(
        Vestiging.objects.values_list('brin')
        .annotate(leerlingen_totaal=Sum('leerlingen'))
        .order_by('brin')
    )

    for year in years:
        if year not in _N_PERSONEN_COLUMNS:
            logger.debug(
                'Skipping year {}.'.format(year))
            continue

        # Create an entry in the LeerlingLeraarRatio Model for each BRIN.
        instances = []
        for brin, group in duo_data.groupby('BRIN NUMMER'):
            if brin not in brin_leerlingen:
                logger.info(
                    'DUO BRIN {} not in Schoolwijzer'.format(brin))

            kwargs = {'brin': brin, 'jaar': year, 'n_leerling': brin_leerlingen.get(brin, None)}
            for _, entry in group.iterrows():
                raw = entry[_N_PERSONEN_COLUMNS[year]]

                n_personen = float(raw)
                target_attr = _TARGET_FUNCTIEGROEP_ATTR[entry['FUNCTIEGROEP']]

                kwargs[target_attr] = n_personen

            instances.append(LeerlingLeraarRatio(**kwargs))

        LeerlingLeraarRatio.objects.bulk_create(instances)

    # TODO: use groupby on the duo_data DataFrame, iterate over all data per school
    # create model instances with all that data (and calculate the ratio).
