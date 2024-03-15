from processing.common.mark_redaction import mark_redaction

import logging

from django.core.management import BaseCommand


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Marks redactions from body_clean and saves in body_redact.'

    def add_arguments(self, parser):
        parser.add_argument('batch_selected', type=int, help='Batch to be marked redacted.')

    def handle(self, *args, **options):
        batch_selected = options['batch_selected']
        mark_redaction(batch_selected)
