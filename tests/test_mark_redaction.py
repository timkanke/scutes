import pytest

from django.core.management import call_command
from src.processing.common.mark_redaction import redact_phonenumbers, redact_using_pattern


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'test_data.yaml')


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('<p>eggs@spam.com</p>',
         '<p><del class="redacted" style="color:red;">eggs@spam.com</del></p>'),
    ]
)
def test_redacted_using_patterns(value, expected):
    result = redact_using_pattern(value)
    assert result == expected


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('<p>515-555-5515</p>',
         '<p><del class="redacted" style="color:red;">515-555-5515</del></p>'),
        ('<p>(515)555-5515</p>',
         '<p><del class="redacted" style="color:red;">(515)555-5515</del></p>'),
         ('<p>(515) 555-5515</p>',
         '<p><del class="redacted" style="color:red;">(515) 555-5515</del></p>'),
    ]
)
def test_redacted_phonenumbers(value, expected):
    result = redact_phonenumbers(value)
    assert result == expected