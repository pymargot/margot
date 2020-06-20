from inspect import getmembers

import pandas as pd

from trading_calendars import get_calendar

from margot.data.column import BaseColumn
from margot.data.features import BaseFeature
from margot.data.ratio import Ratio


class Symbol(object):
    """A Symbol, represents a securitised tradable asset.

    A symbol can contain columns and features as members.

    Usage example::

        class Equity(Symbol):
            adj_close = av.Column(function='historical_daily_adjusted',
                                time_series='adjusted_close')
            log_returns = finance.LogReturns(column='adj_close')
            realised_vol = finance.RealisedVolatility(column='log_returns',
                                                    window=30)

        spy = Equity(symbol='SPY', trading_calendar='NYSE')

    Args:
        symbol (str): the code for this symbol
        trading_calendar (str): ISO Code market identifier
            uses https://github.com/quantopian/trading_calendars/blob/master/README.md
        env (dict): Optional - pass in env values rather than use sysenv.

    """

    def __init__(self, symbol: str, trading_calendar: str, env: dict = {}):  # noqa: D107
        self.symbol = symbol
        self.env = env
        self.trading_calendar = get_calendar(trading_calendar)

        self.columns = [
            member for member,
            ref in getmembers(self, lambda m: isinstance(m, BaseColumn))]

        self.features = [
            member for member,
            ref in getmembers(self, lambda m: isinstance(m, BaseFeature))]

        self.ratios = [
            member for member,
            ref in getmembers(self, lambda m: isinstance(m, Ratio))]

        for col in self.columns:
            new_col = getattr(self, col).clone()
            setattr(self, col, new_col)
            getattr(self, col).setup(symbol=symbol, env=self.env)

        for feature in self.features:
            base_series_name = getattr(self, feature).get_column_name()
            new_feat = getattr(self, feature).clone()
            setattr(self, feature, new_feat)
            base_col = getattr(self, base_series_name)
            getattr(self, feature).set_column(base_col)

        # TODO ratios

        super().__init__()

    def to_dict(self):
        elements = self.columns + self.features + self.ratios
        return {(self.symbol, elt): getattr(self, elt).series
                for elt in elements}

    def to_pandas(self):
        return pd.DataFrame(self.to_dict())

    def refresh(self):
        """Refresh all columns in this Symbol."""
        [getattr(self, member).refresh() for member in self.columns]

    def simulate(self, when=None):
        """Make the Symbol simulate a datetime in history.

        Used for backtesting to simplify the writing of trading
        algorithms.

        Args:
            when (tz_aware datetime or pd.Timestamp): when to go back to.
        """
        for col in self.columns:
            getattr(self, col).simulate(when)

        for feature in self.features:
            getattr(self, feature).simulate(when)

        for ratio in self.ratios:
            getattr(self, ratio).simulate(when)
