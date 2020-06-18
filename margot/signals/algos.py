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
from margot.signals.periods import DAILY
from margot.data import MargotDataFrame


class BaseAlgo(object):
    """A base class to inherit when implementing your trading algorithm.

    You should at least implement signal() which is the output
    of a trading algorithm.

    Args:
        env (dict): a dictionary of environment variables, e.g. API keys.
                    Overrides anything provided in sys env.

    Raises:
        ValueError: the attribute, 'data' must be a reference to a MargotDataFrame.
        NotImplementedError: If your subclass does not implement signal(), you will
            receive a NotImplementedError.

    """

    frequency = DAILY
    data = None

    def __init__(self, env: dict = {}, calendar='XNYS'):  # noqa: D107
        self.env = env
        self.calendar = calendar
        if not isinstance(self.data, MargotDataFrame):
            raise ValueError('Please set data to reference a MargotDataFrame')

    def signal(self) -> list:
        """Return a list of Position objects for a given datetime."""
        raise NotImplementedError("You must implement signal")

    def simulate(self, when: datetime):
        """Simulate a signal from a point in time.

        Args:
            when (datetime): when to go back to

        Returns:
            pd.DataFrame: time-series of Positions.
        """
        self.original_data = deepcopy(self.data)
        self.data.simulate(when)
        positions = self.signal()
        self.data = self.original_data
        return positions

    def run(self, when: datetime = None):
        """Call to run this algo at a point in time (when).

        We store the results of fetch_data() so that we can backtest
        without hitting the data provider more than once.

        :return: a list of Position objects for a given datetime
        """

        if not when:
            when = datetime.now(tz=pytz.UTC)

        return self.signal()
