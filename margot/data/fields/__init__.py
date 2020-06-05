import os
import logging
import pandas as pd


class BaseField(object):
    """A Field represents a single time series of a symbol.

    This could be adjusted_close, open, volume - etc.

    Example: 
        volume = fields.AlphaVantage(function='historical_daily_adjusted', field='adjusted_close')

    Args:
        function (str): the name of the function passed to the Alphavantage API
        field (str): the name of the column that will be returned
    """

    INITED = False
    data = None

    def __init__(self, function, field):
        """Initialise; see class for usage."""
        self.function = function
        self.field = field
        self.series = None

    def _setup(self, symbol: str, env: dict={}):
        self.symbol = symbol
        self.env = env
        self.hdf5_file = os.path.join(env.get('DATA_CACHE'), '{}.hdf5'.format(self.symbol))
        self.INITED = True

    def _load_or_update_series(self):
        raise NotImplementedError('This is implementation specific to the data provider.')

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