import logging

from bs4 import BeautifulSoup

from django.core.management import BaseCommand

from processing.models import Item


logger = logging.getLogger(__name__)


def redact_final(html):
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find_all('del')

    for tag in tags:
        tag.string = '▊▊▊▊▊▊▊▊▊▊'
        tag = tag.unwrap().get_text(strip=True)

    html = str(soup)
    return html


class Command(BaseCommand):
    help = "Finalize redactions from body_redact and saves to body_final."

    def add_arguments(self, parser):
        parser.add_argument('batch_selected', type=int, help='Batch to have redactions finalized.')

    def handle(self, *args, **options):
        items = Item.objects.filter(batch=options['batch_selected'])
        item = Item.objects.all()
        for item in items:
            logger.info(f'Marking: {item.id}, {item.title}')

            html = item.body_redact

            html = redact_final(html)

            item.body_final = html
            item.save(update_fields=['body_final'])
