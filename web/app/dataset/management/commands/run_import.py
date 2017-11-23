"""
Import datasources for onderwijs dashboard.
"""
from django.core.management.base import BaseCommand

from dataset.models import Vestiging
from dataset.import_schoolwijzer import get_vestigingen
from dataset.import_duo import get_leerlingen_naar_gewicht
from dataset.import_duo import get_school_adviezen_from_csv
from dataset.import_duo import get_cito_scores
from dataset.calc_llratio import get_leerling_leraar_ratios

_YEARS = [2011, 2012, 2013, 2014, 2015, 2016]


class Command(BaseCommand):
    help = 'Retrieve onderwijs data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Grabbing data'))
        get_vestigingen()  # TODO: Years?

        brin6s = set(Vestiging.objects.values_list('brin6', flat=True))

        for year in _YEARS:
            print('For year {}'.format(year))
            get_leerlingen_naar_gewicht(year, brin6s)
            get_school_adviezen_from_csv(year, brin6s)
            get_cito_scores(year, brin6s)
        get_leerling_leraar_ratios(_YEARS)
        self.stdout.write(self.style.SUCCESS('Done !!!'))
