import os
import logging
import itertools
from datetime import date, datetime, timedelta

import pandas as pd
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from trading_calendars import get_calendar

import pytz
from margot.periods import DAILY


class BaseAlgo(object):
    """A base class to inherit when implementing your trading algorithm.

    You should at least implement return_position() which is the output
    of a trading algorithm.

    Declare "uses" - which is a list of symbols. These symbols represent
    instruments that are used by / traded by the algo. By declaring them
    in "uses" - build_df will collect price history for those symbols
    and make it available to use in return_position().

    Args:
        env (dict): a dictionary of environment variables, e.g. API keys.
                    Overrides anything provided in sys env.

    Raises:
        ValueError: [description]
        NotImplementedError: [description]

    """

    uses = list()
    mapper = dict()

    frequency = DAILY

    def __init__(self, env: dict, calendar='XNYS'):
        """Init the AlgoMoC class."""
        self.env = env
        self.symbols = dict()
        self.calendar = calendar

    def data_at_date(self, when: datetime) -> pd.DataFrame:
        """Return only the data available on a given trading day.

        That is, the EOD from the previous day.
        :return: Pandas DataFrame()
        """
        return self.df.shift()[:when].copy()

    def return_position(self, df: pd.DataFrame) -> list:
        """Return a list of Position objects for a given datetime."""
        raise NotImplementedError("You must implement return_position")

    def execute(self, when: datetime = None):
        """Call to run this algo at a point in time (when).

        We store the results of fetch_data() so that we can backtest
        without hitting the data provider more than once.

        :return: a list of Position objects for a given datetime
        """
        if not when:
            when = datetime.now(tz=pytz.UTC)

        return self.return_position(
            self.data_at_date(when)
        )
