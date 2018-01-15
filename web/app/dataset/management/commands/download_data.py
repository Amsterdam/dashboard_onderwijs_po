"""
Import datasources for onderwijs dashboard.
"""
import os

from django.core.management.base import BaseCommand, CommandError

from dataset import download_datafiles


class Command(BaseCommand):
    help = 'Download non public onderwijs data files from object store.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir', dest='dir', type=str,
            help='Directory to store the datafiles (default /data).')

    def handle(self, *args, **options):
        self.stdout.write('Downloading datafiles from objectstore.')
        target_dir = options['dir'] if options['dir'] is not None else '/data'
        os.makedirs(target_dir, exist_ok=True)
        content = os.listdir(target_dir)
        if content:
            raise CommandError(
                'Directory (in container!) not empty: {}'.format(target_dir))
        download_datafiles.main(target_dir)
        self.stdout.write('Done')
