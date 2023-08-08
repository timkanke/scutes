import logging
import re
from collections import Counter
from typing import Optional, Pattern, Union

from django.core.management import BaseCommand

from processing.models import Item


logger = logging.getLogger(__name__)

# Regex redaction patterns
REDACT_PATTERNS = {
    'Email address': re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
    'North American phone number': re.compile(r'''
    (\+\d{1,2}([ -]|%20)?)? # optional country code with separator
    \(?\d{3}\)?             # area code
    ([. -]|%20)             # separator
    \d{3}                   # exchange
    ([. -]|%20)             # separator
    \d{4}                   # local
    ''', re.VERBOSE)
}


def redact_using_regex(html):
    return html


def redact_using_string(html):
    return html


class Command(BaseCommand):
    help = "Marks redactions from body_clean and saves in body_redact."

    def add_arguments(self, parser):
        parser.add_argument('batch_selected', type=int, help='Batch to be cleaned.')

    def handle(self, *args, **options):
        items = Item.objects.filter(batch=options['batch_selected'])
        item = Item.objects.all()
        for item in items:
            logger.info('Scanning:', item. id, item.title)

            html = item.body_clean

            html = redact_using_regex(html)
            html = redact_using_string(html)

            item.body_redact = html
            item.save(update_fields=['body_redact'])
