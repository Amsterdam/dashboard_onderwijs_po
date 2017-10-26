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
        get_leerlingen_naar_gewicht()
        get_school_adviezen()
        get_cito_scores()
        get_leerling_leraar_ratios()
        self.stdout.write(self.style.SUCCESS('Done !!!'))
