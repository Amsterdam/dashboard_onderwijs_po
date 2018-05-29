import logging

from django.core.management.base import BaseCommand

from dataset.create_summaries import create_summaries

LOG_FORMAT = '%(asctime)-15s - %(name)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Summarize onderwijs data (what is present for which school).'

    def handle(self, *args, **options):
        create_summaries()
