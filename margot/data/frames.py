from inspect import getmembers
from datetime import datetime

import pandas as pd

from margot.data.column import BaseColumn
from margot.data.features import BaseFeature
from margot.data.symbols import Symbol
from margot.data.ratio import Ratio


class MargotDataFrame(object):
    """A MargotDataFrame brings together symbols, columns, features and ratios.

    Example::

        class Equity(Symbol):
            adj_close = av.Column(function='historical_daily_adjusted',
                                  time_series='adjusted_close')
            log_returns = finance.LogReturns(column='adj_close')
            realised_vol = finance.RealisedVolatility(column='log_returns',
                                                      window=30)

        class ExampleDF(MargotDataFrame):
            spy = Equity(symbol='SPY', trading_calendar='NYSE')
            vtwo = Equity(symbol='VTWO', trading_calendar='NYSE')
            spy_russ_ratio = Ratio(numerator=spy.adj_close,
                                   denominator=vtwo.adj_close,
                                   label='spy_russ')

        mydf = ExampleDF()

    Args:
        env (dict): optional env dictionary as an alternative to sysenv
            variables.

    """

    def __init__(self, env: dict = {}):   # noqa: D107
        self.env = env

        self.symbols = [
            name for name,
            ref in getmembers(self, lambda m: isinstance(m, Symbol))]

        self.features = [
            name for name,
            ref in getmembers(self, lambda m: isinstance(m, BaseFeature))]

        self.ratios = [
            name for name,
            ref in getmembers(self, lambda m: isinstance(m, Ratio))]
        super().__init__()

    def to_pandas(self, periods: int = None, dropna=True) -> pd.DataFrame:
        """Return a pandas Dataframe representing this MargotDataFrame.

        Args:
            periods (int, optional): only return the tail n periods.

        Returns:
            pd.DataFrame: a Pandas dataframe representing all data from
                the MargotDataFrame
        """
        # Get the elements one at a time, to pandas them and ensemble.
        if len(self.symbols) == 1:
            df1 = self.symbols[0].to_pandas()
        elif len(self.symbols) > 1:
            df1 = pd.concat([getattr(self, name).to_pandas()
                             for name in self.symbols], axis=1)
        else:
            df1 = pd.DataFrame()

        df2 = pd.DataFrame({('margot', name): getattr(self, name).series
                            for name in self.ratios + self.features})

        df = pd.concat([df1, df2], axis=1)

        if dropna:
            df = df.dropna()

        if periods:
            df = df.tail(periods)

        return df

    def refresh(self):
        """Refresh all Symbols in this DataFrame."""
        for member in self.symbols:
            getattr(self, member).refresh()
        # TODO what about ratios?

    @property
    def start_date(self):
        """First Timestamp of the time-series index.

        Returns:
            Timestamp: a pandas timestamp.
        """
        return self.to_pandas().index.min()

    @property
    def end_date(self):
        """Last Timestamp value of the time-series index.

        Returns:
            Timestamp: a pandas timestamp.
        """
        return self.to_pandas().index.max()

    @property
    def index(self):
        """Return the time-series index.

        Returns:
            pd.Index: a pandas timeseries index.
        """
        return self.to_pandas().index

    @property
    def when(self):
        return self._when

    @when.setter
    def set_when(self, when):  # noqa: D102
        self._when = when

    def simulate(self, when):
        """Create a dataframe simulating a datetime in history.

        Used for backtesting to simplify the writing of trading
        algorithms. After simulating a historical datetime, it is
        not possible to go back to the future.

        Args:
            when (tz_aware datetime or pd.Timestamp): when to go back to.
        """
        self._when = when

        for symbol in self.symbols:
            getattr(self, symbol).simulate(when)

        for feature in self.features:
            getattr(self, feature).simulate(when)

        for ratio in self.ratios:
            getattr(self, ratio).simulate(when)

    def end_simulation(self):
        self._when = None

        for symbol in self.symbols:
            getattr(self, symbol).simulate()

        for feature in self.features:
            getattr(self, feature).simulate()

        for ratio in self.ratios:
            getattr(self, ratio).simulate()
