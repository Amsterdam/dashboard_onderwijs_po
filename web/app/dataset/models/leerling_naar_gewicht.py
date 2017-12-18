"""
Deal with DUO Leerling naar gewicht data set.
"""
from django.db import models
import pandas

from dataset.models.vestiging import Vestiging

_LEERLING_GEWICHT = {
    'GEWICHT_0': '0',
    'GEWICHT_0.3': '0.3',
    'GEWICHT_1.2': '1.2',
}


class LeerlingNaarGewichtManager(models.Manager):
    def import_csv(self, uri, year, brin6s):
        df = pandas.read_csv(
            uri,
            delimiter=';',
            # dtype=_SCHOOLADVIEZEN_CSV_COLUMNS,  # TODO: add this extra safety
            encoding='cp1252'
        )
        mask = df['GEMEENTENUMMER'] == 363  # only Amsterdam is relevant

        instances = []
        for i, row in df[mask].iterrows():
            brin6 = row['BRIN_NUMMER'] + '{:02d}'.format(int(row['VESTIGINGSNUMMER']))

            # voor ieder gewicht maken we een entry
            for column, value in _LEERLING_GEWICHT.items():  # py3!
                obj = LeerlingNaarGewicht(
                    brin=row['BRIN_NUMMER'],
                    vestigingsnummer=row['VESTIGINGSNUMMER'],

                    gewicht=value,
                    totaal=row[column],
                    jaar=year,
                )

                obj.vestiging_id = brin6 if brin6 in brin6s else None
                instances.append(obj)

        self.bulk_create(instances)


class LeerlingNaarGewicht(models.Model):
    class Meta:
        unique_together = ('brin', 'vestigingsnummer', 'jaar', 'gewicht')

    brin = models.CharField(max_length=4)
    vestigingsnummer = models.IntegerField()

    gewicht = models.CharField(max_length=3)
    totaal = models.IntegerField()
    jaar = models.IntegerField()
    vestiging = models.ForeignKey(
        Vestiging,
        on_delete=models.SET_NULL,
        null=True,
        related_name='leerling_naar_gewicht',
    )

    # peildatum = models.DateField()  # TODO: see whether we need peildatum
    objects = LeerlingNaarGewichtManager()
