import os
import logging
from pathlib import Path

import pandas as pd


class BaseColumn(object):
    """A Column represents a single time series of a symbol.

    This could be adjusted_close, open, volume - etc.

    Example:
        volume = column.AlphaVantage(function='historical_daily_adjusted', field='adjusted_close')

    Args:
        function (str): the name of the function passed to the Alphavantage API
        column (str): the name of the column that will be returned
    """

    INITED = False
    data = None

    def __init__(self, function, column):
        """Initialise; see class for usage."""
        self.function = function
        self.column = column
        self.series = None

    def get_label(self):
        return self.column

    def _setup(self, symbol: str, env: dict = {}):
        self.symbol = symbol
        self.env = env

        # TODO this should be handled somewhere central in a configuration
        # thingo.
        data_cache = env.get('DATA_CACHE', os.environ.get('DATA_CACHE'))
        Path(data_cache).mkdir(parents=True, exist_ok=True)

        self.hdf5_file = os.path.join(
            data_cache, '{}.hdf5'.format(
                self.symbol))
        self.INITED = True

    def _load_or_update_series(self):
        raise NotImplementedError(
            'This is implementation specific to the data provider.')

    def save(self):
        """Save it."""
        self.data.to_hdf(self.hdf5_file, key='adjusted_close')
        logging.debug('Symbol {} saved'.format(self.symbol))

    def load(self):
        """Load it."""
        self.data = pd.read_hdf(
            self.hdf5_file,
            key='adjusted_close').sort_index()
        logging.debug('Symbol {} loaded'.format(self.symbol))

    def get_series(self):
        """Get the data series as a pandas series.

        Returns:
            pd.Series: time series of the field
        """
        if self.series:
            return self.series
        else:
            return self._load_or_update_series()
