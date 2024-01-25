import logging

from django.core.management import BaseCommand

from processing.common.finalize_redactions import convert_redaction


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Finalize redactions from body_redact and saves to body_final.'

    def add_arguments(self, parser):
        parser.add_argument('batch_selected', type=int, help='Batch to have redactions finalized.')

    def handle(self, *args, **options):
        batch_selected = batch=options['batch_selected']
        convert_redaction(batch_selected)
