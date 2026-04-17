#!/usr/bin/env python

import datetime

import pytest
from freezegun import freeze_time

from pydeckard import utils


@freeze_time("2019-05-16 13:35:16")
def test_since_second():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert utils.since(ref) == "1 second"


@freeze_time("2019-05-16 13:35:21")
def test_since_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert utils.since(ref) == "6 seconds"


@freeze_time("2019-05-16 13:36:21")
def test_since_minute_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert utils.since(ref) == "1 minute 6 seconds"


@freeze_time("2019-05-16 13:37:21")
def test_since_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert utils.since(ref) == "2 minutes 6 seconds"


@freeze_time("2019-05-16 14:37:21")
def test_since_hour_and_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert utils.since(ref) == "1 hour 2 minutes 6 seconds"


@freeze_time("2019-05-16 15:37:21")
def test_since_hours_and_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert utils.since(ref) == "2 hours 2 minutes 6 seconds"


@freeze_time("2019-05-17 15:37:21")
def test_since_day_hours_and_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert utils.since(ref) == "1 day 2 hours 2 minutes 6 seconds"


@freeze_time("2019-05-19 15:37:21")
def test_since_days_hours_and_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert utils.since(ref) == "3 days 2 hours 2 minutes 6 seconds"


if __name__ == "__main__":
    pytest.main()
