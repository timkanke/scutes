from bs4 import BeautifulSoup
import pytest

from src.processing.management.commands.finalize_redactions import redact_final


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('<html><body><del class="redacted" style="color:red;">kent.brockman@springfield.com</del></body></html>',
         '<html><body>▊▊▊▊▊▊▊▊▊▊</body></html>'),
    ]
)
def test_redact_final(value, expected):
    html = value
    result = str(redact_final(html))
    assert result == expected
