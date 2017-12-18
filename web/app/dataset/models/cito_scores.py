"""
Module met modellen voor Cito scores uit DUO data.
"""
from django.db import models

from .vestiging import Vestiging


class DUOAPIManagerMixin:
    def from_duo_api_json(self, data, year, brin6s):
        instances = []
        for entry in data['results']:
            instances.append(self._from_duo_api_json_entry(entry, year, brin6s))
        self.bulk_create(instances)


class CitoScoresManager(models.Manager, DUOAPIManagerMixin):
    def _from_duo_api_json_entry(self, json_dict, year, brin6s):
        brin6 = json_dict['BRIN_NUMMER'] + \
            '{:02d}'.format(int(json_dict['VESTIGINGSNUMMER']))

        # Usage of case is not consistent over the years (in the data).
        upper = {key.upper(): key for key in json_dict}

        leerjaar8 = json_dict[upper['LEERJAAR_8']]
        raw = json_dict[upper['CET_GEM']].strip()

        # CITO scores can be missing
        cet_gem = raw.replace(',', '.') if raw else None

        obj = CitoScores(
            brin=json_dict['BRIN_NUMMER'],
            vestigingsnummer=json_dict['VESTIGINGSNUMMER'],
            cet_gem=cet_gem,
            leerjaar_8=leerjaar8,
            jaar=year,
        )
        obj.vestiging_id = brin6 if brin6 in brin6s else None
        return obj


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
