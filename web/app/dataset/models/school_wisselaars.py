from django.db import models
from openpyxl import load_workbook
import pandas

from .vestiging import Vestiging


def _detect_duplicate_brin6(dataframe):
    """
    Detect duplicated BRIN 6 codes (with different school names).
    """
    # TODO: proper logging
    mask = dataframe.duplicated(subset=['brin6'])
    duplicated_brin6s = set(dataframe[mask]['brin6'])

    for brin6 in duplicated_brin6s:
        print('Gedupliceerde BRIN6 {} wordt overgeslagen'.format(brin6))
        for i, row in dataframe[dataframe['brin6'] == brin6]:
            print('  {}: {}'.format(row['brin6'], row['schoolnaam']))

    return duplicated_brin6s


class SchoolWisselaarsManager(models.Manager):
    def _from_excel_file(self, file_name, year, brin6s):
        """
        Load Excel file of "schoolwisselaars", save to db.
        """
        # Load the Excel workbook, convert to Pandas DataFrame
        ws = load_workbook(file_name)['schoolwisseling in 2016 perc']
        data = ws.values
        columns = next(data)
        df = pandas.DataFrame(data, columns)

        # Detect / report duplicate BRIN 6 codes.
        duplicated_brin6s = _detect_duplicate_brin6(df)

        # Create instances
        instances = []
        for i, row in df.iterrows():
            if row['brin6'] in duplicated_brin6s:
                continue  # Skip records with duplicated BRIN 6 codes

            brin = row['brin6'][:4]
            vestigingsnummer = int(row['brin6'][4:])

            obj = SchoolWisselaars(
                brin=brin,
                vestigingsnummer=vestigingsnummer,
                naam=row['schoolnaam'],  # potential duplicate of Vestiging naam
                wisseling_uit=row['wisseling_uit'],
                wisseling_in=row['wisseling_in'],
                jaar=year,
            )

            brin6 = row['brin6']
            obj.vestiging_id = brin6 if brin6 in brin6s else None
            instances.append(obj)

        self.bulk_create(instances)


class SchoolWisselaars(models.Model):
    brin = models.CharField(max_length=4)
    vestigingsnummer = models.IntegerField()

    naam = models.CharField(max_length=255)
    wisseling_uit = models.FloatField()
    wisseling_in = models.FloatField()

    jaar = models.IntegerField()
    vestiging = models.ForeignKey(
        Vestiging, related_name='schoolwisselaars', null=True)
