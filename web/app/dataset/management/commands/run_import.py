"""
Import datasources for onderwijs dashboard.
"""
from django.core.management.base import BaseCommand

from dataset.import_schoolwijzer import get_vestigingen
from dataset.import_duo import get_leerlingen_naar_gewicht
from dataset.import_duo import get_school_adviezen
from dataset.import_duo import get_cito_scores
from dataset.import_duo import get_leerling_leraar_ratios


class Command(BaseCommand):
    help = 'Retrieve onderwijs data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Grabbing data'))
        get_vestigingen()
        get_leerlingen_naar_gewicht(2014)
        get_school_adviezen(2013)
        get_cito_scores(2014)
        get_leerling_leraar_ratios(2014)
        self.stdout.write(self.style.SUCCESS('Done !!!'))
