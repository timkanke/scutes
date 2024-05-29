from bs4 import BeautifulSoup
import pytest

from src.processing.management.commands.clean import cleaner, emoji_fixer, ltr_messages, \
      ms_messages, remove_p_br_p, replace_pre_with_p, remove_mailto, remove_tel


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('<html><body><p><br></p></body></html>',
         '<html><body><p></p></body></html>'),
    ]
)
def test_remove_p_br_p(value, expected):
    soup = BeautifulSoup(value, 'lxml')
    result = str(remove_p_br_p(soup))
    assert result == expected


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('<html><body><pre>First line.\nNext line.</pre></body></html>',
         '<html><body><p>First line.<br/>Next line.</p></body></html>'),
    ]
)
def test_replace_pre_with_p(value, expected):
    result = replace_pre_with_p(value)
    assert result == expected


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('<head><meta></head><body><style></style><div class="WordSection1"><p class="MsoNormal">Text</p></div></body>',
         '<p>Text<br/><br/></p>'),
    ]
)
def test_ms_messages(value, expected):
    soup = BeautifulSoup(value, 'lxml')
    result = str(ms_messages(soup))
    assert result == expected


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('<p class="p1" style="margin: 0px; font-stretch: normal;"><span class="s2">Text</span></p>',
         '<html><body><span class="s2">Text</span><br/></body></html>'),
    ]
)
def test_ltr_messages(value, expected):
    soup = BeautifulSoup(value, 'lxml')
    result = str(ltr_messages(soup))
    assert result == expected


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('🎧  🍿🤏😯',
         '&#127911;  &#127871;&#129295;&#128559;'),
    ]
)
def test_emoji_fixer(value, expected):
    result = emoji_fixer(value)
    assert result == expected


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('<a href="mailto:name@example.com">name@example.com</a>',
         '<html><body>name@example.com</body></html>'),
    ]
)
def test_remove_mailto(value, expected):
    soup = BeautifulSoup(value, 'lxml')
    result = str(remove_mailto(soup))
    assert result == expected


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('<a href="tel:555-555-5555">555-555-5555</a>',
         '<html><body>555-555-5555</body></html>'),
    ]
)
def test_remove_tel(value, expected):
    soup = BeautifulSoup(value, 'lxml')
    result = str(remove_tel(soup))
    assert result == expected


def test_cleaner(shared_datadir):
    expected = (shared_datadir / "test_clean/cleaner_expected.html").read_text()
    value = (shared_datadir / "test_clean/cleaner_value.html").read_text()
    result = cleaner(value)
    assert expected == result
