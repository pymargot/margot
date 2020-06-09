import os
import logging
from pathlib import Path
import pytz
import pandas as pd


class BaseColumn(object):
    """A Column represents a single time series of a symbol.

    This could be adjusted_close, open, volume - etc.

    Example:
        volume = column.AlphaVantage(function='historical_daily_adjusted', field='adjusted_close')

    Args:
        function (str): the name of the function passed to the Alphavantage API
        time_series (str): the name of the time_series that will be returned
    """

    INITED = False
    data = None

    def __init__(self, function, time_series: str):
        """Initialise; see class for usage."""
        self.function = function
        self.time_series = time_series
        self.series = None

    def get_label(self):
        return self.series.name

    def setup(self, symbol: str, env: dict = {}):
        self.symbol = symbol
        self.env = env

        # TODO File names should be managed in a central configuration
        data_cache = env.get('DATA_CACHE', os.environ.get('DATA_CACHE'))
        Path(data_cache).mkdir(parents=True, exist_ok=True)

        self.hdf5_file = os.path.join(
            data_cache, '{}.hdf5'.format('strategy'))
        self.series = self.load_or_fetch_series()
        self.INITED = True

    def clean(self, df):
        """Clean the df."""
        df = df.sort_index()
        # Ensure the index is TZ aware.
        df = df.tz_localize(pytz.UTC)
        # Standardise the column names
        df = df.rename(mapper={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. adjusted close': 'adjusted_close',
            '6. volume': 'volume',
            '7. dividend amount': 'divident_amount',
            '8. split coefficient': 'split_coefficient'
        }, axis='columns')
        return df

    def load_or_fetch_series(self):
        """[summary]

        Returns:
            pd.Series: time series of the field
        """
        try:
            self.df = self.load(self.symbol)
        except KeyError:
            self.df = self.fetch(self.symbol)
            self.save()
        return self.df[self.time_series]

    def fetch(self, symbol: str):
        raise NotImplementedError(
            'This is implementation specific to the data provider.')

    def save(self):
        """Save it."""
        self.df.to_hdf(self.hdf5_file, key=self.symbol)

    def load(self, symbol: str):
        """Load it."""
        return pd.read_hdf(
            self.hdf5_file,
            key=symbol).sort_index().copy()

    def get_series(self):
        """Get the data series as a pandas series.

        Returns:
            pd.Series: time series of the field
        """
        if self.INITED:
            return self.series
        else:
            raise LookupError('Column not inited.')
