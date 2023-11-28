import logging
import mailbox
import re

from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from pathlib import Path

from django.core.management import BaseCommand

from processing.models import Batch, File, Item

logger = logging.getLogger(__name__)

# Reporter Processing
reporter_scrub = [
    ', Senior White House Correspondent',
    'via All',
    'EOP/WHO',
]

reporter_extract = re.compile(
    r"""
    ^
    ["\' ]*     # ignore punctuation and whitespace
    (.*?)       # reporter name (minimal match)
    ["\' ]*     # ignore punctuation and whitespace
    (?:\(.+\))? # ignore a title or organization in parentheses
    ["\' ]*     # ignore punctuation and whitespace
    <.*>        # ignore the email address
    $
""",
    re.VERBOSE,
)


def process_reporter(reporter: str) -> str:
    """Build the Reporter field from the message From header."""

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
            reporter = s[1] + ' ' + s[0]

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
    (
        r'-- \nTo unsubscribe from this group and stop receiving emails from it, send an email to all\+unsubscribe@.*\.com\.',
        '',
    ),  # noqa
    (
        r'-- \<br /\>\nTo unsubscribe from this group and stop receiving emails from it, send an email to \<a href\="mailto\:all\+unsubscribe@.*\.com"\>all\+unsubscribe@.*\.com\</a\>\.\<br /\>',
        '',
    ),  # noqa
]

p_charset = re.compile(r'charset=[a-zA-Z0-9-]+')


def scrub_body(html: str) -> str:
    # Scrub specific string values
    for old, new in body_scrub:
        html = re.sub(old, new, html, re.DOTALL)
        logger.debug(f'body: scrubbed "{old}"')
    # Update the charset since we have convert to utf-8
    html = p_charset.sub('charset=utf-8', html)
    return html


# Determine pool_report to be true or false
# https://docs.python.org/3/library/re.html
# r'\b...\b' is for matching "whole words"
NONPOOL_REPORT_MARKERS = [
    re.compile('[Dd]ear [Cc]olleagues'),
    re.compile('[Hh]ello [Cc]olleagues'),
    re.compile('Colleagues'),
    re.compile('OFF RECORD', re.IGNORECASE),
    re.compile('off the record', re.IGNORECASE),
    re.compile(r'\bFPPO\b'),
    re.compile('non-reportable', re.IGNORECASE),
    re.compile(r'\breportable\b', re.IGNORECASE),
]


def is_pool_report(html: str) -> bool:
    """
    Returns True if the given HTML appears to be pool report, False
    otherwise.
    """
    for marker in NONPOOL_REPORT_MARKERS:
        if marker.search(html):
            return False

    return True


class Command(BaseCommand):
    help = 'Loads data from mbox into database.'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='File path to be imported.')

    def handle(self, *args, **options):
        file_path = Path(options['file_path'])
        file_name = Path(file_path).stem

        batch = Batch()
        batch.name = file_name
        batch.save()

        for message in mailbox.mbox(file_path):
            item = Item()
            logger.debug(f'{item=}')

            # Date
            date = parsedate_to_datetime(message['Date']).isoformat()
            item.date = date
            logger.debug(date)

            # Reporter
            From, encoding = decode_header(message['From'])[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            item.reporter = process_reporter(From)
            logger.debug(item.reporter)

            # Title
            subject, encoding = decode_header(message['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding)
            item.title = scrub_title(subject)
            logger.debug(item.title)

            # Body
            for part in message.walk():
                content_type = part.get_content_type()
                if content_type in ('text/html'):
                    logger.debug('Found HTML body for message')
                    content = part.get_payload(decode=True)
                    charset = part.get_content_charset()
                    logger.debug(charset)
                    if charset is None:
                        charset = 'UTF-8'
                    html = content.decode(charset)
                elif content_type in ('text/plain'):
                    logger.debug('Found plain text body for message')
                    content = part.get_payload(decode=True)
                    charset = part.get_content_charset()
                    logger.debug(charset)
                    if charset is None:
                        charset = 'UTF-8'
                    text = content.decode(charset)
                    html = f'<html><body><pre>{text}</pre></body></html>'
                elif content_type in (''):
                    logger.warning('Unable to find body for message')
                    html = ''
            item.body_original = scrub_body(html)

            # Checkboxes
            item.pool_report = is_pool_report(html)
            item.publish = False
            item.off_the_record = False
            item.review_status = False

            # fk
            item.batch = batch

            # attachment
            """
            Value class for holding information about files associated with a message.

            Attributes
            ----------
            filename: str
                The filename from the message
            content: bytes
                 The contents of the message file
            output_subdir: str
                When writing to output, the subdirectory to output to. Default
                is '', which writes to the message folder
            content_id: str
                The content id associated with the file. Defaults to '', which
                indicates no content id. Typically used for matching attachments to
                in-line image links in the message.
            """
            file = File()
            for part in message.walk():
                filename = part.get_filename()
                if filename:
                    content = part.get_payload(decode=True)
                    content_id = part['Content-ID']
                    file.file = content
                    file.title = decode_header(part.get_filename())[0][1]

            item.save()
