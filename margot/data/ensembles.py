from inspect import getmembers

import pandas as pd 

from margot.data.column import BaseColumn
from margot.data.feature import BaseFeature
from margot.data.symbols import Symbol
from margot.data.ratio import Ratio


class Ensemble(object):
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
            column_name = getattr(self, column).column
            base_series = getattr(self, column_name).get_series()
            getattr(self, feature)._setup(base_series=base_series)

    def to_pandas(self):
        ### Get the elements one at a time, to pandas them and ensemble.
        df = pd.DataFrame()
        df_list = [getattr(self, symbol).to_pandas() for symbol in self.symbols]
        return pd.concat(df_list)