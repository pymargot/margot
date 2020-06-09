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

    def __init__(self, function, time_series: str):
        """Initialise; see class for usage."""
        self.function = function
        self.time_series = time_series
        self.series = None

    def get_label(self):
        """Return the label for this column."""
        return self.series.name

    def clone(self):
        """Return a new instance of oneself."""
        return self.__class__(self.function, self.time_series) 

    def setup(self, symbol: str, env: dict = {}):
        """Setup the column. Called by the Symbol so that the symbol name
         can be passed.
        """
        self.symbol = symbol
        self.env = env

        # TODO File names should be managed in a central configuration
        data_cache = env.get('DATA_CACHE', os.environ.get('DATA_CACHE'))
        Path(data_cache).mkdir(parents=True, exist_ok=True)

        self.hdf5_file = os.path.join(
            data_cache, '{}.hdf5'.format('strategy'))

    def clean(self, df):
        """Clean the df."""
        df = df.sort_index()
        # Ensure the index is TZ aware.
        if df.index.tz is None:
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

    def load_or_fetch_series(self, symbol: str):
        """[summary]

        Returns:
            pd.Series: time series of the field
        """
        try:
            df = self.load(symbol)
        except (KeyError, FileNotFoundError):
            df = self.fetch(symbol)
            self.save(df, symbol)
        return df[self.time_series]

    def fetch(self, symbol: str):
        raise NotImplementedError(
            'This is implementation specific to the data provider.')

    def load(self, symbol: str):
        """Load it."""
        return pd.read_hdf(
            self.hdf5_file,
            key=symbol)

    def save(self, df, symbol):
        """Save it."""
        df.to_hdf(self.hdf5_file, key=symbol)

    def get_series(self):
        """Get the data series as a pandas series.

        Returns:
            pd.Series: time series of the field
        """
        if self.series is None:
            self.series = self.load_or_fetch_series(self.symbol)
            self.INITED = True
            return self.series
        else:
            return self.series
