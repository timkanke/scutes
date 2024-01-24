import logging

from bs4 import BeautifulSoup

from processing.models import Item

logger = logging.getLogger(__name__)


def redact_final(html):
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find_all('del', {'class': 'redacted'})

    for tag in tags:
        new_string = '▊▊▊▊▊▊▊▊▊▊'
        tag = tag.replace_with(new_string)

    html = str(soup)
    return html


def convert_redaction(batch_selected):
    items = Item.objects.filter(batch=batch_selected)
    item = Item.objects.all()
    logger.info(f'Converting Batch {batch_selected}')
    for item in items:
        logger.info(f'Marking: {item.id}, {item.title}')
        yield f'Converting: {item.id}, {item.title}<br>'
        html = item.body_redact
        html = redact_final(html)
        item.body_final = html
        item.save(update_fields=['body_final'])
    yield f'Completed Converting Batch {batch_selected}'
