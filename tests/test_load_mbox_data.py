import pytest

from src.processing.common.load_mbox_data import is_pool_report, process_reporter, scrub_title, scrub_body


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('"Kent Brockman" <brockman@springfieldgazette.com>',
         'Kent Brockman'),
        ('"Brockman, Kent" <brockman@springfieldgazette.com>',
         'Kent Brockman'),
        ('"Brockman, Kent , Senior White House Correspondent" <brockman@springfieldgazette.com>',
         'Kent Brockman'),
    ]
)
def test_process_reporter(value, expected):
    reporter = value
    result = process_reporter(reporter)
    assert result == expected


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('[WH Pool] Travel pool report #7a: more deets on location and memorial service',
         'Travel pool report #7a: more deets on location and memorial service'),
    ]
)
def test_scrub_title(value, expected):
    title = value
    result = scrub_title(title)
    assert result == expected


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('''-- \nTo unsubscribe from this group and stop receiving emails from it, send an email to all+unsubscribe@example.com.''', ''),  # noqa
        ('''-- <br />\nTo unsubscribe from this group and stop receiving emails from it, send an email to <a href="mailto:all+unsubscribe@example.com">all+unsubscribe@example.com</a>.<br />''', '')  # noqa
    ]
)
def test_scrub_body(value, expected):
    html = value
    result = scrub_body(html)
    assert result == expected


def test_is_pool_report_true():
    # All POOL_REPORT_EXAMPLES should return true
    for index, report in enumerate(POOL_REPORT_EXAMPLES):
        assert is_pool_report(report), f"Report {index} not recognized as a pool report"


def test_is_pool_report_false():
    # All NONPOOL_REPORT_EXAMPLES should return false
    for index, report in enumerate(NONPOOL_REPORT_EXAMPLES):
        assert not is_pool_report(report), f"Report {index} incorrectly considered a pool report"


# All of the following are valid pool reports
POOL_REPORT_EXAMPLES = [
    '''\
    Behind the outdoor stage ... on the deck.
    The audience was a few hundred people.
    The president said the ...
    "The world is watching you," he told workers. "Our nation ..."

    Pool is being moved out near end of speech.
    ''',

    '''\
    At 4:48 local time headed back to Green Bay.
    ''',

    '''\
    Reporters gaggled on ... did a TV spot on ...

    Smith, however, declined to take questions as he walked back to the West Wing.
    ''',
]

# All of the following are not pool reports
NONPOOL_REPORT_EXAMPLES = [
    '''\
    FPPO version with times attached.
    ''',
    '''\
    Flagging for all, off the record.  From WH:

    NPS/USSS will be ..., from 4:30 AM to 7 AM. This will cause a ... when entering.
    ''',
    '''\
     Reportable week ahead from the White House is below. FPPO version to follow, sometime later today."
    ''',
    '''\
    OFF RECORD/FPPO

    Dear colleagues,

    We are writing ...
    '''
]
