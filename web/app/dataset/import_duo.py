"""
Import code for DUO data sets.
"""
# flake8: noqa

# TODO items:
# * consider using DRF serializers for creating new Model instances
# * investigate whether JSON-LD can be used directly to validate received data
# * remove debug prints, replace with logging where needed

import json

import requests
import pandas
from jsonschema import validate
from dataset.models import LeerlingenNaarGewicht
from dataset.models import SchoolAdviezen
from dataset.models import CitoScores

from dataset.models import Vestiging
from django.conf import settings


_BASE_API_URL = 'https://api.duo.nl/v0/datasets/'

_LEERLINGEN_NAAR_GEWICHT = '02.leerlingen-bo-swv-vestiging%2C-gewicht%2C-impulsgebied%2C-schoolgewicht-{start}-{end}/search'
_SCHOOL_ADVIEZEN = '04.-leerlingen-bo-sbo-schooladviezen-{start}-{end}/search'
_CITO_SCORES = '05.-gemiddelde-eindscores-bo-sbo-{start}-{end}/search'

# -- leerlingen naar gewicht ---

def _handle_leerlingen_naar_gewicht(json_dict):
    return LeerlingenNaarGewicht(
        brin=json_dict['BRIN_NUMMER'],
        vestigingsnummer=json_dict['VESTIGINGSNUMMER'],

        gewicht_0=json_dict['GEWICHT_0'],
        gewicht_0_3=json_dict['GEWICHT_0.3'],
        gewicht_1_2=json_dict['GEWICHT_1.2'],
        # TODO: add peildatum, jaar
    )


def get_leerlingen_naar_gewicht(year):
    DATA_SET = _LEERLINGEN_NAAR_GEWICHT.format(start=year, end=year+1)
    PARAMETERS = {'uni_gemeentenaam': 'amsterdam'}
    API_URL = requests.compat.urljoin(_BASE_API_URL, DATA_SET)

    result = requests.get(API_URL, PARAMETERS)
    assert result.status_code == 200

    data = json.loads(result.text)
    instances = []
    for entry in data['results']:
        instances.append(_handle_leerlingen_naar_gewicht(entry))

    LeerlingenNaarGewicht.objects.bulk_create(instances)
    tmp = LeerlingenNaarGewicht.objects.count()
    print('Number of results leerlingen naar gewicht', len(data['results']))
    print('  Number of leerlingen naar gewicht in DB', tmp)



# -- school adviezen --

def _handle_school_adviezen(json_dict):
    return SchoolAdviezen(
        brin=json_dict['BRIN_NUMMER'],
        vestigingsnummer=json_dict['VESTIGINGSNUMMER'],

        vmbo_bl=json_dict['VMBO_BL'],
        vmbo_bl_kl=json_dict['VMBO_BL_KL'],
        vmbo_gt=json_dict['VMBO_GT'],
        vmbo_gt_havo=json_dict['VMBO_GT_HAVO'],
        vmbo_kl=json_dict['VMBO_KL'],
        vmbo_kl_gt=json_dict['VMBO_KL_GT'],
        vso=json_dict['VSO'],
        vwo=json_dict['VWO'],
    )


def get_school_adviezen(year):
    # TODO: consider downloading CSV in stead of going through API
    DATA_SET = _SCHOOL_ADVIEZEN.format(start=year, end=year+1)
    PARAMETERS = {'uni_gemeentenaam': 'amsterdam'}
    API_URL = requests.compat.urljoin(_BASE_API_URL, DATA_SET)
    print('Retrieving', API_URL)

    result = requests.get(API_URL, PARAMETERS)
    assert result.status_code == 200

    data = json.loads(result.text)
    instances = []
    for entry in data['results']:
        instances.append(_handle_school_adviezen(entry))
    SchoolAdviezen.objects.bulk_create(instances)
    tmp = SchoolAdviezen.objects.count()
    print('Number of School Adviezen entries:', len(data['results']))
    print('  Number of School Adviezen in DB:', tmp)


# -- Cito scores --

def _handle_cito_scores(json_dict):
    return CitoScores(
        brin=json_dict['BRIN_NUMMER'],
        vestigingsnummer=json_dict['VESTIGINGSNUMMER'],

        cet_gem=json_dict['cet_gem'].replace(',', '.'),
        leerjaar_8=json_dict['Leerjaar_8']
    )


def get_cito_scores(year):
    DATA_SET = _CITO_SCORES.format(start=year, end=year+1)
    PARAMETERS = {'uni_gemeentenaam': 'amsterdam'}
    API_URL = requests.compat.urljoin(_BASE_API_URL, DATA_SET)
    print('Retrieving', API_URL)

    result = requests.get(API_URL, PARAMETERS)
    assert result.status_code == 200

    data = json.loads(result.text)
    instances = []
    for entry in data['results']:
        instances.append(_handle_cito_scores(entry))

    CitoScores.objects.bulk_create(instances)
    tmp = CitoScores.objects.count()
    print('Number of CITO scores entries:', len(data['results']))
    print('  Number of CITO scores in DB:', tmp)


# -- leerling leraar ratio --


def get_leerling_leraar_ratios(year):
    DATA_SET_URL = 'https://duo.nl/open_onderwijsdata/images/01.-po-personen-owtype-bestuur-brin-functie.csv'

    # Style: process full datafile in memory, than drop clean data in database.
    # TODO: seems to be availabel per BRIN, not vestiging -> check

    df = pandas.read_csv(DATA_SET_URL, delimiter=';', decimal='.')

    brin_nummers = Vestiging.objects.values_list('brin', flat=True).distinct()
    print('Brin nummers', brin_nummers)
    print('Aantal BRIN nummers in Amsterdam', len(brin_nummers))
    relevant = df.loc[df['BRIN NUMMER'].isin(brin_nummers)]

    brin_nummers_duo = set(df['BRIN NUMMER'])

    print('Alleen in Amsterdamse data:')
    print(set(brin_nummers) - brin_nummers_duo)

    vestigingen = list(Vestiging.objects.all())

    ##

