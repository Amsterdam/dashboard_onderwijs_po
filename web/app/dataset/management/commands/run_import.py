"""
Import datasources for onderwijs dashboard.
"""
from django.core.management.base import BaseCommand

from dataset.import_schoolwijzer import get_vestigingen
from dataset.import_duo import get_leerlingen_naar_gewicht
from dataset.import_duo import get_school_adviezen
from dataset.import_duo import get_cito_scores
from dataset.calc_llratio import get_leerling_leraar_ratios


class Command(BaseCommand):
    help = 'Retrieve onderwijs data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Grabbing data'))
        get_vestigingen()  # Years?

        for year in [2011, 2012, 2013, 2014, 2015, 2016]:
            print('For year {}'.format(year))
            get_leerlingen_naar_gewicht(year)
            get_school_adviezen(year)
            get_cito_scores(year)
        get_leerling_leraar_ratios([2015])
        self.stdout.write(self.style.SUCCESS('Done !!!'))
