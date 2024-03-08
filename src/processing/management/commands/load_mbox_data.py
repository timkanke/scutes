from processing.common.load_mbox_data import load_data

import logging

from pathlib import Path

from django.core.management import BaseCommand
from processing.models import Batch

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Loads data from mbox into database.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='File path to be imported.')

    def handle(self, *args, **options):
        file_path = Path(options['file_path'])

        batch_name = Path(file_path).stem
        batch = Batch()
        batch.name = batch_name
        logger.debug(f'Batch Name: {batch_name}')
        batch.save()
        batch_id = batch.id
        logger.debug(f'Batch ID: {batch_id}')

        load_data(file_path, batch_id)
