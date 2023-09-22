import logging
import re

from django.core.management import BaseCommand

from processing.models import Item, Redact


logger = logging.getLogger(__name__)

'''
Built-in Redaction Pattern

North American phone number matches the following:
000-000-0000
000 000 0000
000.000.0000

(000)000-0000
(000)000 0000
(000)000.0000
(000) 000-0000
(000) 000 0000
(000) 000.0000

000-0000
000 0000
000.0000

0000000
0000000000
(000)0000000
'''
REDACT_PATTERNS = {
    'Email address': re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"),
    'North American phone number': re.compile(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"),
}


def redact_using_pattern(html):
    while True:
        for label, pattern in REDACT_PATTERNS.items():
            match = re.findall(pattern, html)
            logger.debug(f'{match}, {label}, {type(match)}')
            string = (str(match))[2:-2]
            html = re.sub(pattern, '<del class="redacted" style="color:red;">'+string+'</del>', html)
            logger.debug(html)
        return html


def redact_using_string(html):
    name = 'redact_list'  # Row name for Redact.object
    if Redact.objects.filter(name=name).exists():
        strings = Redact.objects.get(name=name).string
        # Object format example: {"label0": "spam", "label1": "eggs"}
        logger.debug(f'{strings} {type(strings)}')
        strings = list(zip(strings.keys(), strings.values()))

        while True:
            for label, pattern in strings:
                match = re.findall(pattern, html)
                logger.debug(f'{match}, {label}, {type(match)}')
                html = re.sub(pattern, '<del class="redacted" style="color:red;">'+pattern+'</del>', html)
                logger.debug(html)
            return html
    else:
        return html


class Command(BaseCommand):
    help = "Marks redactions from body_clean and saves in body_redact."

    def add_arguments(self, parser):
        parser.add_argument('batch_selected', type=int, help='Batch to be marked redacted.')

    def handle(self, *args, **options):
        items = Item.objects.filter(batch=options['batch_selected'])
        item = Item.objects.all()
        for item in items:
            logger.info(f'Marking: {item.id}, {item.title}')

            html = item.body_clean

            html = redact_using_pattern(html)
            html = redact_using_string(html)

            item.body_redact = html
            item.save(update_fields=['body_redact'])
