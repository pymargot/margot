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

    def simulate_signal(self, when: datetime):
        """Simulate a signal from a point in time.

        Stores the original MargotDataFrame referenced by self. data
        on a temporary reference so that the data attribute can be
        used by signal() to calculate positions at a point in history.

        After running signal(), the full dataframe is re-referenced
        at self.data. 

        Args:
            when (datetime): when in history to go back to

        Returns:
            list: a list of Position objects.
        """
        self.original_data = deepcopy(self.data)
        self.data.simulate(when)
        positions = self.signal()
        self.data = self.original_data
        return positions
