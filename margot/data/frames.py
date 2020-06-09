from inspect import getmembers

import pandas as pd

from margot.data.column import BaseColumn
from margot.data.feature import BaseFeature
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
        super().__init__()

    def get_elements(self):
        self.symbols = [
            ref for member,
            ref in getmembers(self, lambda m: isinstance(m, Symbol))]

        self.features = [
            ref for member,
            ref in getmembers(self, lambda m: isinstance(m, BaseFeature))]

        self.ratios = [
            ref for member,
            ref in getmembers(self, lambda m: isinstance(m, Ratio))]
        return self.symbols + self.features + self.ratios

    def to_pandas(self):
        # Get the elements one at a time, to pandas them and ensemble.
        df_list = [ref.to_pandas() for ref in self.get_elements()]
        return pd.concat(df_list, axis=1)
