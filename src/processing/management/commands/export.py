import logging

from django.core.management import BaseCommand

from processing.models import Item


logger = logging.getLogger(__name__)

OUTPUT_COLUMNS = [
    'Identifier',
    'Title',
    'Date',
    'Creator',
    'Object Type',
    'Format',
    'Rights Statement',
    'FILES'
]


def create_csv():
    pass


def create_files():
    pass


class Command(BaseCommand):
    help = "Exports batch"

    def add_arguments(self, parser):
        parser.add_argument('batch_selected', type=int, help='Batch to be exported.')

    def handle(self, *args, **options):
        items = Item.objects.filter(batch=options['batch_selected'])
        item = Item.objects.all()
        for item in items:
            logger.info(f'Exporting: {item.id}, {item.title}')
