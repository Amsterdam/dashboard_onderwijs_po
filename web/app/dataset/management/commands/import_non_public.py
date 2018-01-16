from django.core.management.base import BaseCommand

from dataset.models import Vestiging
from dataset.import_non_public import get_subsidies
from dataset.import_non_public import get_schoolwisselaars
from dataset.import_non_public import report_rows

_YEARS = [2011, 2012, 2013, 2014, 2015, 2016, 2017]


class Command(BaseCommand):
    help = 'Load priviliged data'

    def handle(self, *args, **options):
        self.stdout.write('Loading priviliged data.')
        brin6s = set(Vestiging.objects.values_list('brin6', flat=True))
        assert brin6s

        for year in _YEARS:
            get_subsidies(year, brin6s)

        for year in _YEARS:
            get_schoolwisselaars(year, brin6s)

        report_rows()
