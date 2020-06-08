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

        self.symbols = [
            member for member,
            ref in getmembers(self) if isinstance(
                ref,
                Symbol)]

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

    def _get_elements(self):
        return self.symbols + self.features + self.ratios

    def to_pandas(self):
        # Get the elements one at a time, to pandas them and ensemble.
        df_list = list()
        for elt in self._get_elements():
            df = getattr(self, elt).to_pandas()
            df_list.append(df)
        return pd.concat(df_list, axis=1)
