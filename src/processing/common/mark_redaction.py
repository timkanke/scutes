import logging
import re

from bs4 import BeautifulSoup as Soup

from processing.models import Item


logger = logging.getLogger(__name__)

"""
Built-in Redaction Pattern

Phone number matches are:
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

# Country code
+00 000 000 0000
+00.000.000.0000
+00-000-000-0000
+000000000000
+00 (000)000 0000

0000 0000000000
0000-000-000-0000
00000000000000
0000 (000)000-0000
"""
REDACT_PATTERNS = {
    'Email address': re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'),
    'Phone number': re.compile(
        r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
    ),
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


def mark_redaction(batch_selected):
    items = Item.objects.filter(batch=batch_selected)
    item = Item.objects.all()
    for item in items:
        logger.info(f'Marking: {item.id}, {item.title}')
        html = item.body_clean
        html = redact_using_pattern(html)
        item.body_redact = html
        item.save(update_fields=['body_redact'])
