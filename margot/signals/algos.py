import os
import logging
import itertools
from datetime import date, datetime, timedelta
from copy import deepcopy

import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from trading_calendars import get_calendar

import pytz

from margot.signals.order_types import MOC, MKT, LMT
from margot import MargotDataFrame


class BaseAlgo(object):
    """A base class to inherit when implementing your trading algorithm.

    You should at least implement signal() which is the output
    of a trading algorithm.

    Args:
        env (dict): a dictionary of environment variables, e.g. API keys.
            Overrides anything provided in sys env.
        market (str): The ISO code for the market we will use.

    Raises:
        ValueError: the attribute, 'data' must be a reference to a MargotDataFrame.
        NotImplementedError: If your subclass does not implement signal(), you will
            receive a NotImplementedError.

    """

    MOC = MOC
    MKT = MKT
    LMT = LMT

    MONDAY = 'MON'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = 'THU'
    FRIDAY = 'FRI'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'

    data = None

    def __init__(self, env: dict = {}, market='XNYS'):  # noqa: D107
        self.env = env
        self.market = get_calendar(market)
        self.when = None
        if not isinstance(self.data, MargotDataFrame):
            raise ValueError('Please set data to reference a MargotDataFrame')

    def weekday(self, dt):
        """Return a human readable three letter day of week.

        Convert the Python integer representation of day of week into a string.

        e.g::

            0: 'MON' (also known as self.MONDAY)

        .. note::
            You should always use the built in constants when passing days of
            the week. e.g. self.MONDAY, self.TUESDAY, ... these map to the three
            charater strings.


        Args:
            dt (datetime or pd.Timestamp): The datetime to check

        Returns:
            str: One of; 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'
        """
        days = {
            0: self.MONDAY,
            1: self.TUESDAY,
            2: self.WEDNESDAY,
            3: self.THURSDAY,
            4: self.FRIDAY,
            5: self.SATURDAY,
            6: self.SUNDAY
        }
        return days.get(dt.weekday())

    @property
    def next_close(self):
        """Return a UTC pd.Timestamp of the next close of trading session.

        Returns:
            pd.Timestamp: Timestamp of the next close of cash session in UTC.
        """
        return self.market.next_close(
            getattr(self, 'when', 
            pd.Timestamp(datetime.now(tz=pytz.UTC)))
            )

    def signal(self) -> list:
        """Return a list of Position objects for a given datetime."""
        raise NotImplementedError("You must implement signal")

    def simulate_signal(self, when: datetime):
        """Simulate a signal from a point in time.

        Stores the original MargotDataFrame referenced by self.data
        on a temporary reference so that the data attribute can be
        used by signal() to calculate positions at a point in history.

        After running signal(), the full dataframe is re-referenced
        at self.data.

        Args:
            when (datetime): when in history to go back to

        Returns:
            list: a list of Position objects.
        """
        self.data.simulate(when)
        self.when = when
        positions = self.signal()
        self.data.end_simulation()
        return positions
