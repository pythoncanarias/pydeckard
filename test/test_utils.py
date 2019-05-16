#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import pytest
import utils


def test_since_second():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    now = datetime.datetime(2019, 5, 16, 13, 35, 16)
    assert utils.since(now, ref) == '1 second'


def test_since_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    now = datetime.datetime(2019, 5, 16, 13, 35, 21)
    assert utils.since(now, ref) == '6 seconds'


def test_since_minute_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    now = datetime.datetime(2019, 5, 16, 13, 36, 21)
    assert utils.since(now, ref) == '1 minute 6 seconds'


def test_since_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    now = datetime.datetime(2019, 5, 16, 13, 37, 21)
    assert utils.since(now, ref) == '2 minutes 6 seconds'


def test_since_hour_and_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    now = datetime.datetime(2019, 5, 16, 14, 37, 21)
    assert utils.since(now, ref) == '1 hour 2 minutes 6 seconds'


def test_since_hours_and_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    now = datetime.datetime(2019, 5, 16, 15, 37, 21)
    assert utils.since(now, ref) == '2 hours 2 minutes 6 seconds'


def test_since_day_hours_and_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    now = datetime.datetime(2019, 5, 17, 15, 37, 21)
    assert utils.since(now, ref) == '1 day 2 hours 2 minutes 6 seconds'


def test_since_days_hours_and_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    now = datetime.datetime(2019, 5, 19, 15, 37, 21)
    assert utils.since(now, ref) == '3 days 2 hours 2 minutes 6 seconds'


if __name__ == "__main__":
    pytest.main()
