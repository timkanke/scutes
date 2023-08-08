import emoji
import logging

from bs4 import BeautifulSoup
from html_sanitizer import Sanitizer  # type: ignore

from django.core.management import BaseCommand

from processing.models import Item


logger = logging.getLogger(__name__)


def remove_p_br_p(soup):
    matches = soup.find_all('p')

    for match in matches:
        just_br = match.find_all('br')
        for x in just_br:
            x.extract()

    return soup


def replace_pre_with_p(html):
    """Replaces pre tag with p tag and line breaks with br"""

    if '<pre>' in html:
        html = html.replace("\n", "<br>")
        soup = BeautifulSoup(html, 'lxml')
        while True:
            tag = soup.find('pre')
            if not tag:
                break
            tag.name = 'p'
        html = str(soup)
        return html
    else:
        return html


def ms_messages(soup):
    for tag in soup(['head', 'style', 'meta']):
        tag.extract()

    empty_whitelist = ['a', 'img']
    while True:
        tag = soup.find('div', class_="WordSection1")
        if not tag:
            break
        tag.name = 'p'
        for x in soup.find_all():
            if len(x.get_text(strip=False)) == 0 and (x.name not in empty_whitelist):
                x.extract()

        for tag in soup(['p']):
            tag.append(soup.new_tag('br'))
        for tag in soup(['p', 'html', 'div']):
            tag.unwrap()
        tag_body = soup.body
        tag_body.name = 'p'

    return soup


def ltr_messages(soup):
    for tag in soup('p', class_='p1'):
        tag.append(soup.new_tag('br'))
    for tag in soup('span', class_='s1'):
        tag.wrap(soup.new_tag('b'))
    for tag in soup('p', class_='p1'):
        tag.unwrap()

    return soup


def xml_escape(chars, data_dict):
    """Emoji encoding helps ensure successful html-sanitizer processing"""
    return chars.encode('ascii', 'xmlcharrefreplace').decode()


def emoji_fixer(html, replace=xml_escape):
    """Emoji encoding helps ensure successful html-sanitizer processing"""
    html = emoji.replace_emoji(html, replace=xml_escape)
    return html


def cleaner(html):
    """Sanitizes the HTML"""

    sanitizer = Sanitizer({
        "tags": {
            # Text Tags
            'p', 'br', 'hr', 'div',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'strong', 'em', 'sub', 'sup', 'u', 'i', 'b',
            'blockquote', 'cite', 'q',

            # Link and Image Tags
            'a', 'img',

            # List Tags
            'ul', 'ol', 'li', 'dl', 'dt', 'dd',

            # Table Tags
            'table', 'tr', 'td', 'th', 'tbody', 'thead', 'tfoot', 'col', 'colgroup', 'caption'
        },

        "attributes": {"a": ("href", "name", "target", "title", "id", "rel"),
                       "img": ("src", "name", "alt", "height"),
                       },
        "empty": {"hr", "a", "br", "img", "col"},
        "separate": {"a", "li"},
        "whitespace": set(),
        "keep_typographic_whitespace": False,
        "add_nofollow": False,
        "autolink": False,
        "element_preprocessors": [],
        "element_postprocessors": [],
        "is_mergeable": lambda e1, e2: False,
        })

    html = sanitizer.sanitize(html)
    return html


class Command(BaseCommand):
    help = "Cleans data from body_original and saves in body_clean."

    def add_arguments(self, parser):
        parser.add_argument('batch_selected', type=int, help='Batch to be cleaned.')

    def handle(self, *args, **options):
        items = Item.objects.filter(batch=options['batch_selected'])
        item = Item.objects.all()
        for item in items:
            logger.info('Cleaning:', item. id, item.title)

            html = item.body_original
            soup = BeautifulSoup(html, 'lxml')
            soup = remove_p_br_p(soup)

            html = str(soup)
            html = replace_pre_with_p(html)

            soup = BeautifulSoup(html, 'lxml')
            soup = ms_messages(soup)
            soup = ltr_messages(soup)

            html = str(soup)
            html = emoji_fixer(html, replace=xml_escape)
            html = cleaner(html)

            item.body_clean = html
            item.save(update_fields=['body_clean'])
