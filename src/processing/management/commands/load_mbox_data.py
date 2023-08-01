import mailbox
import re
import email
from csv import DictReader
from email import policy
from email.header import decode_header, make_header
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
import logging
from pathlib import Path

from django.core.management import BaseCommand

from processing.models import Batch, Item

logger = logging.getLogger(__name__)

# Reporter Processing
reporter_scrub = [
    ', Senior White House Correspondent',
    'via All',
    'EOP/WHO',
]

reporter_extract = re.compile(r'''
    ^
    ["\' ]*     # ignore punctuation and whitespace
    (.*?)       # reporter name (minimal match)
    ["\' ]*     # ignore punctuation and whitespace
    (?:\(.+\))? # ignore a title or organization in parentheses
    ["\' ]*     # ignore punctuation and whitespace
    <.*>        # ignore the email address
    $
''', re.VERBOSE)


def process_reporter(reporter: str) -> str:
    """ Build the Reporter field from the message From header. """

    logger.debug(f'reporter: From={reporter}')

    for scrub in reporter_scrub:
        if scrub in reporter:
            reporter = reporter.replace(scrub, '')
            logger.debug(f'reporter: scrubbed "{scrub}": {reporter}')

    if m := reporter_extract.match(reporter):
        s = re.split(r' *, *', m[1])
        if len(s) == 1:
            reporter = s[0]
        else:
            # Change "LastName, FirstName" to "FirstName LastName"
            # Ignore anything after a second comma
            reporter = s[1] + " " + s[0]

        logger.debug(f'reporter: extracted: {reporter}')

    return reporter


# Processing Title
title_scrub = [
    '[WH Pool] ',
    '\n',
]


def scrub_title(value: str) -> str:
    """
    Build the Title field from the message Subject header.
    """
    logger.debug(f'title: Subject={value}')

    for scrub in title_scrub:
        if scrub in value:
            value = value.replace(scrub, '')
            logger.debug(f'title: scrubbed "{scrub}": {value}')

    # escape any backslashes and pipe characters
    value = re.sub(r'([\\|])', r'\\\1', value)

    return value


# Body Processing
body_scrub = [
                '''-- \nTo unsubscribe from this group and stop receiving emails from it, send an email to all+unsubscribe@whpoolreports.com.''',  # noqa
                '''-- <br />\nTo unsubscribe from this group and stop receiving emails from it, send an email to <a href="mailto:all+unsubscribe@whpoolreports.com">all+unsubscribe@whpoolreports.com</a>.<br />''',  # noqa
            ]

p_charset = re.compile(r'charset=[a-zA-Z0-9-]+')


def scrub_body(html: str) -> str:
    # Scrub specific string values
    for scrub in body_scrub:
        if scrub in html:
            html = html.replace(scrub, '')
            logger.debug(f'body: scrubbed "{scrub}"')
    # Update the charset since we have convert to utf-8
    html = p_charset.sub("charset=utf-8", html)
    return html


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from mbox into database."

    def handle(self, *args, **options):
        path = Path('../tests/scutes/test_data')
        file_name = Path('apple.mbox')

        batch = Batch()
        batch.name = file_name.stem
        batch.save()

        for message in mailbox.mbox(path / file_name):
            item = Item()

            # Date
            date = parsedate_to_datetime(message['Date']).isoformat()
            item.date = date

            # Reporter
            reporter = message['From']
            item.reporter = process_reporter(reporter)

            # Title
            title = message['Subject']
            item.title = scrub_title(title)

            # Checkboxes
            item.pool_report = False
            item.publish = False
            item.off_the_record = False
            item.review_status = False

            # Body
            for part in message.walk():
                content_type = part.get_content_type()
                if content_type in ('text/html'):
                    content = part.get_payload(decode=True)
                    charset = part.get_content_charset()
                    if charset is None:
                        charset = 'UTF-8'
                    html = content.decode(charset)
                elif content_type in ('text/plain'):
                    content = part.get_payload(decode=True)
                    charset = part.get_content_charset()
                    if charset is None:
                        charset = 'UTF-8'
                    text = content.decode(charset)
                    html = f"<html><body><pre>{text}</pre></body></html>"
                elif content_type in (''):
                    logger.warning(f'Unable to find body for message')
                    html = ""
            item.body_original = scrub_body(html)

            # fk
            item.batch = Batch(batch.pk)

            item.save()


"""
TO DO
- modify pool_report to detect true/false
- modify input of file name and path instead of hard coded
- automate it! determine how new files will be discovered when script runs
- add tests
- remove test data from .gitignore
"""
