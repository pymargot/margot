from inspect import getmembers

import pandas as pd

from margot.data.column import BaseColumn
from margot.data.feature import BaseFeature
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

    def __init__(self, symbol: str, env: dict = {}):
        """Initiate."""
        self.symbol = symbol
        self.env = env
        self.columns = [
            member for member,
            ref in getmembers(self) if isinstance(
                ref,
                BaseColumn)]

        self.features = [
            member for member,
            ref in getmembers(self) if isinstance(
                ref,
                BaseFeature)]

        self.ratios = [
            member for member,
            ref in getmembers(self) if isinstance(
                ref,
                Ratio)]

        for column in self.columns:
            getattr(self, column)._setup(symbol=self.symbol, env=self.env)

        for feature in self.features:
            column_name = getattr(self, column).time_series
            base_series = getattr(self, column_name).get_series()
            getattr(self, feature)._setup(base_series=base_series)

    def to_dict(self):
        elements = self.columns + self.features + self.ratios
        return {(self.symbol, elt): getattr(self, elt).get_series()
                for elt in elements}

    def to_pandas(self):
        return pd.DataFrame(self.to_dict())
