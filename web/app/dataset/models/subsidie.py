import logging

from django.db import models
from openpyxl import load_workbook
import pandas

from .vestiging import Vestiging
from .school_wisselaars import _detect_duplicate_brin6, _is_brin6

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SubsidieManager(models.Manager):
    def _from_excel(self, file_name, year, brin6s):
        # temp:
        Subsidie.objects.all().delete()
        # Load the Excel workbook, convert to Pandas DataFrame
        logger.info('Creating Subsidie entries')

        ws = load_workbook(filename=file_name)['Blad1']
        columns = [x.value for x in ws[4]]
        data = ([x.value for x in row] for row in ws.iter_rows(min_row=5))
        df = pandas.DataFrame(data, columns=columns)

        # for consistency with other data sets:
        df.rename(
            index=str,
            columns={
                'School brin': 'brin6',
                'School naam': 'schoolnaam',
            },
            inplace=True
        )

        # create entries in database for each subsidie
        duplicated_brin6s = _detect_duplicate_brin6(df)
        instances = []
        for i, row in df.iterrows():
            if row['brin6'] in duplicated_brin6s:
                continue
            if not _is_brin6(row['brin6']):
                continue

            brin = row['brin6'][:4]
            vestigingsnummer = int(row['brin6'][4:])

            for key, value in row[2:].iteritems():
                if not pandas.isnull(value):
                    # for now only awarded subsidies are stored
                    obj = Subsidie(
                        brin=brin,
                        vestigingsnummer=vestigingsnummer,
                        jaar=year,
                        naam=key,
                    )
                    brin6 = row['brin6']
                    obj.vestiging_id = brin6 if brin6 in brin6s else None
                    instances.append(obj)

        self.bulk_create(instances)


# The names and available subsidies may vary over the years, so each individual
# subsidy has an entry.
class Subsidie(models.Model):
    brin = models.CharField(max_length=4)
    vestigingsnummer = models.IntegerField()

    jaar = models.IntegerField()
    naam = models.CharField(max_length=255)
    vestiging = models.ForeignKey(
        Vestiging, related_name='subsidies', null=True)

    objects = SubsidieManager()
