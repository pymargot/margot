from inspect import getmembers

import pandas as pd

from margot.data.column import BaseColumn
from margot.data.features import BaseFeature
from margot.data.symbols import Symbol
from margot.data.ratio import Ratio


class MargotDataFrame(object):
    """An Ensemble brings together symbols, columns and features.

    Args:
        object ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """

    def __init__(self, env: dict = {}):
        """Initiate."""
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

    def to_pandas(self):
        # Get the elements one at a time, to pandas them and ensemble.
        df = pd.concat([getattr(self, name).to_pandas()
                        for name in self.symbols], axis=1)

        df2 = pd.DataFrame({('margot', name): getattr(self, name).get_series()
                            for name in self.ratios + self.features})
        return pd.concat([df, df2], axis=1)

    def refresh(self):
        """Refresh all Symbols in this DataFrame."""
        for member in self.symbols:
            getattr(self, member).refresh() 
