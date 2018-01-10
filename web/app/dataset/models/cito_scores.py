"""
Module met modellen voor Cito scores uit DUO data.
"""
import pandas
from django.db import models

from .vestiging import Vestiging


class UpperCaseKeyDict(dict):
    def __getitem__(self, key):
        return super(UpperCaseKeyDict, self).__getitem__(key.upper())


_CITO_SCORES_CSV_COLUMNS = UpperCaseKeyDict([
    ('PEILDATUM_LEERLINGEN', str),
    ('PRIKDATUM_SCORES', str),
    ('BRIN_NUMMER', str),
    ('VESTIGINGSNUMMER', int),
    ('INSTELLINGSNAAM_VESTIGING', str),
    ('POSTCODE_VESTIGING', str),
    ('PLAATSNAAM', str),
    ('GEMEENTENUMMER', int),
    ('GEMEENTENAAM', str),
    ('PROVINCIE', str),
    ('SOORT_PO', str),
    ('DENOMINATIE_VESTIGING', str),
    ('BEVOEGD_GEZAG_NUMMER', int),
    ('LEERJAAR_8', int),
    ('ONTHEFFING_REDEN_ND', int),
    ('CET_AANTAL', int),
    ('CET_GEM', float),
    ('IEP_AANTAL', float),
    ('ROUTE8_AANTAL', int),
    ('ROUTE8_GEM', float),
    ('DIA_AANTAL', int),
    ('DIA_GEM', float),
    ('CESAN_AANTAL', int),
    ('AMN_AANTAL', int),
    ('AMN_GEM', float),
])


class DUOAPIManagerMixin:
    def from_duo_api_json(self, data, year, brin6s):
        instances = []
        for entry in data['results']:
            instances.append(self._from_duo_api_json_entry(entry, year, brin6s))
        self.bulk_create(instances)


class CitoScoresManager(models.Manager, DUOAPIManagerMixin):
    def import_csv(self, uri, year, brin6s):
        df = pandas.read_csv(
            uri,
            delimiter=';',
            dtype=_CITO_SCORES_CSV_COLUMNS,
            encoding='cp1252',
            decimal=',',
            na_values=[' '],
        )
        df = df.rename(columns=str.upper)

        mask = df['GEMEENTENUMMER'] == 363

        instances = []
        for i, row in df[mask].iterrows():
            brin6 = row['BRIN_NUMMER'] + '{:02d}'.format(int(row['VESTIGINGSNUMMER']))
            obj = CitoScores(
                brin=row['BRIN_NUMMER'],
                vestigingsnummer=row['VESTIGINGSNUMMER'],
                cet_gem=row['CET_GEM'],
                leerjaar_8=row['LEERJAAR_8'],
                jaar=year,
            )
            obj.vestiging_id = brin6 if brin6 in brin6s else None
            instances.append(obj)
        self.bulk_create(instances)


class CitoScores(models.Model):
    """Shadow relevant parst of CITO Scores dataset of DUO."""
    # TODO: peildatum  / prikdatum
    class Meta:
        unique_together = ('brin', 'vestigingsnummer', 'jaar')

    brin = models.CharField(max_length=4)
    vestigingsnummer = models.IntegerField()

    cet_gem = models.FloatField(null=True)
    leerjaar_8 = models.IntegerField(null=True)
    jaar = models.IntegerField()
    vestiging = models.ForeignKey(
        Vestiging,
        on_delete=models.SET_NULL,
        related_name='cito_scores',
        null=True
    )

    objects = CitoScoresManager()
