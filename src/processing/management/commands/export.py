import logging

from pathlib import Path

from django.core.management import BaseCommand

from processing.common.export import export


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Exports batch'

    def add_arguments(self, parser):
        parser.add_argument('batch_selected', type=int, help='Batch to be exported.')
        parser.add_argument('file_path', type=str, help='File path to export.')

    def handle(self, *args, **options):
        batch_selected = options['batch_selected']
        export_path = Path(options['file_path'])
        export(batch_selected, export_path)