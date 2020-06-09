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
            ref in getmembers(self, lambda m: isinstance(m, BaseColumn))]

        self.features = [
            member for member,
            ref in getmembers(self, lambda m: isinstance(m, BaseFeature))]

        self.ratios = [
            member for member,
            ref in getmembers(self, lambda m: isinstance(m, Ratio))]

        for column in self.columns:
            getattr(self, column).setup(symbol=self.symbol, env=self.env)

        super().__init__()

    def to_dict(self):
        elements = self.columns + self.features + self.ratios
        return {(self.symbol, elt): getattr(self, elt).get_series()
                for elt in elements}

    def to_pandas(self):
        return pd.DataFrame(self.to_dict())
