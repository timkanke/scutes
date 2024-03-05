from processing.common.clean import clean

import logging

from django.core.management import BaseCommand


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Cleans data from body_original and saves in body_clean.'

    def add_arguments(self, parser):
        parser.add_argument('batch_selected', type=int, help='Batch to be cleaned.')

    def handle(self, *args, **options):
        batch_selected = options['batch_selected']
        clean(batch_selected)
