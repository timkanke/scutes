import pytest

from src.processing.management.commands.mark_redaction import redact_using_patterns, redact_using_string


# TODO Requires test database setup
@pytest.mark.django_db(True)
@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('<p>eggs</p>',
         '<p><del class="redacted" style="color:red;">eggs</del></p>'),
    ]
)
def test_redact_using_string(value, expected):
    # result = redact_using_string(value)
    # print(result)
    # assert result == expected
    pass


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('<p>eggs@spam.com</p>',
         '<p><del class="redacted" style="color:red;">eggs@spam.com</del></p>'),
    ]
)
def test_redacted_using_patterns(value, expected):
    result = redact_using_patterns(value)
    assert result == expected
