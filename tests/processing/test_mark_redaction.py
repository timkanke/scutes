import pytest

from django.core.management import call_command
from src.processing.management.commands.mark_redaction import redact_using_pattern, redact_using_string


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'test_data.yaml')


# TODO Requires fixture or test database setup
@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('<p>eggs</p>',
         '<p><del class="redacted" style="color:red;">eggs</del></p>'),
    ]
)
def test_redact_using_string(db, django_db_setup, value, expected):
    result = redact_using_string(value)
    print(result)
    assert result == expected


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
