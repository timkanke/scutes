import logging
import phonenumbers
import re

from bs4 import BeautifulSoup as Soup

from processing.models import Item


logger = logging.getLogger(__name__)


REDACT_PATTERNS = {
    'Email address': re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'),
}


def redact_using_pattern(html):
    for label, pattern in REDACT_PATTERNS.items():
        matches = re.findall(pattern, html)
        for match in matches:
            logger.debug(f'{match}, {label}, {type(match)}')
            string = str(match)
            html = re.sub(match, '<del class="redacted" style="color:red;">' + string + '</del>', html)
        logger.debug(html)
    return html


def redact_phonenumbers(html):
    numbers = phonenumbers.PhoneNumberMatcher(html, "US")
    for number in numbers:
        logger.debug(number)
        string = number.raw_string
        html = html.replace(string, '<del class="redacted" style="color:red;">' + string + '</del>')
    logger.debug(html)
    return html


def mark_redaction(batch_selected):
    items = Item.objects.filter(batch=batch_selected)
    item = Item.objects.all()
    for item in items:
        logger.info(f'Marking: {item.id}, {item.title}')
        html = item.body_clean
        html = redact_using_pattern(html)
        html = redact_phonenumbers(html)
        item.body_redact = html
        item.save(update_fields=['body_redact'])
