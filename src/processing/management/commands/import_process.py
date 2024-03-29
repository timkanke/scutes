from processing.common.clean import clean
from processing.common.load_mbox_data import load_data
from processing.common.mark_redaction import mark_redaction

import logging

from pathlib import Path

from django.core.management import BaseCommand
from processing.models import Batch


logger = logging.getLogger(__name__)


def import_batch(file_path):
    batch_name = Path(file_path).stem
    batch = Batch()
    batch.name = batch_name
    logger.debug(f'Batch Name: {batch_name}')
    batch.save()
    batch_id = batch.id
    logger.debug(f'Batch ID: {batch_id}')
    load_data(file_path, batch_id)
    batch_selected = str(batch_id)
    clean(batch_selected)
    mark_redaction(batch_selected)


class Command(BaseCommand):
    help = 'Imports, cleans, and marks redactions data.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='File path to be imported.')

    def handle(self, *args, **options):
        file_path = Path(options['file_path'])
        files = []
        existing_batchs = list(Batch.objects.all().values_list('name', flat=True))
        existing_batchs = [existing_batch + '.mbox' for existing_batch in existing_batchs]

        for file in file_path.iterdir():
            if file.suffix == '.mbox':
                files.append(str(file.name))
        for i in files[:]:
            if i in existing_batchs:
                files.remove(i)
        files = [str(file_path) + '/' + file for file in files]
        files.sort()
        logger.info(f'Files import list: {files}')

        for file_path in files:
            logger.debug(f'Importing: {file_path}')
            import_batch(file_path)

        logger.info('Import Complete')
