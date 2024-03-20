import logging

from pathlib import Path

from django.core.management import BaseCommand

from processing.common.convert_and_export import convert_and_export


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Converts and Exports batch'

    def add_arguments(self, parser):
        parser.add_argument('batch_selected', type=int, help='Batch to be exported.')

    def handle(self, *args, **options):
        batch_selected = options['batch_selected']
        convert_and_export(batch_selected)
