import logging

from django.core.management.base import BaseCommand
from django.db.models import Avg
from dataset.models import LeerlingLeraarRatio
from dataset.models import CitoScores

_YEARS = [2011, 2012, 2013, 2014, 2015, 2016]

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# TODO: validate these calculations with the client


class Command(BaseCommand):
    help = 'Populate aggregate fields on models'

    def handle(self, *args, **options):
        for year in _YEARS:
            self.stdout.write('Calculating aggregates (relevant averages).')

            # Update all city wide average Leerling-Leraar Ratio's
            llr_avg = (
                LeerlingLeraarRatio.objects.all()
                .filter(jaar__exact=year)
                .exclude(n_onderwijzend__isnull=True)
                .exclude(n_onderwijzend__exact=0)
                .aggregate(Avg('n_onderwijzend'))
            )
            (
                LeerlingLeraarRatio.objects.all()
                .filter(jaar__exact=year)
                .update(n_onderwijzend_avg=llr_avg['n_onderwijzend__avg'])
            )

            self.stdout.write(
                'Gemiddelde Leerling-Leeraar ratio: {}'.format(llr_avg))

            # Update all city wide average CITO scores for this year
            cito_scores_avg = (
                CitoScores.objects.all()
                .filter(jaar__exact=year)
                .exclude(cet_gem__isnull=True)
                .exclude(cet_gem__exact=0)
                .aggregate(Avg('cet_gem'))
            )
            (
                CitoScores.objects.all()
                .filter(jaar__exact=year)
                .update(cet_gem_avg=cito_scores_avg['cet_gem__avg'])
            )

            self.stdout.write('Gemiddelde CITO score: {}'.format(cito_scores_avg))

            # TODO: switch this to annotations (neater)
            # TODO: integrate this with standard import pipeline
