from inspect import getmembers

import pandas as pd

from trading_calendars import get_calendar

from margot.data.column import BaseColumn
from margot.data.features import BaseFeature
from margot.data.ratio import Ratio


class Symbol(object):
    """A Symbol, that has columns and features.

    Args:
        object ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """

    def __init__(self, symbol: str, trading_calendar: str, env: dict = {}):    # noqa: D107
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

        super().__init__()

    def to_dict(self):
        elements = self.columns + self.features + self.ratios
        return {(self.symbol, elt): getattr(self, elt).get_series()
                for elt in elements}

    def to_pandas(self):
        return pd.DataFrame(self.to_dict())

    def refresh(self):
        """Refresh all columns in this Symbol."""
        [getattr(self, member).refresh() for member in self.columns]