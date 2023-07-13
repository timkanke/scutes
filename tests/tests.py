import pytest


def test_pytest():
    assert True


@pytest.mark.webdriver
def test_selenium(selenium):
    selenium.get('http://www.example.com')
