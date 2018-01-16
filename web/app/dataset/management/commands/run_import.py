"""
Import datasources for onderwijs dashboard.
"""
import logging

from django.core.management.base import BaseCommand

from dataset.import_schoolwijzer import get_vestigingen
from dataset.import_duo import get_leerling_naar_gewicht
from dataset.import_duo import get_school_advies
from dataset.import_duo import get_cito_scores
from dataset.calc_llratio import get_leerling_leraar_ratios

from dataset.models import Vestiging
from dataset.models import SchoolType
from dataset.models import report_rows

_YEARS = [2011, 2012, 2013, 2014, 2015, 2016]

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Retrieve onderwijs data.'

    def handle(self, *args, **options):
        SchoolType.objects.create_known()

        self.stdout.write(self.style.SUCCESS('Grabbing data'))
        get_vestigingen()  # TODO: Think about history (schoolwijzer keeps none)

        brin6s = set(Vestiging.objects.values_list('brin6', flat=True))

        for year in _YEARS:
            print('For year {}'.format(year))
            get_school_advies(year, brin6s)
            get_leerling_naar_gewicht(year, brin6s)
            get_cito_scores(year, brin6s)
        get_leerling_leraar_ratios(_YEARS)
        self.stdout.write(self.style.SUCCESS('Done !!!'))

        report_rows()
        self.stdout.write('Done!')
