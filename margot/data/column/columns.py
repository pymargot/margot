import os
import logging
from pathlib import Path
import pytz
import pandas as pd


class BaseColumn(object):
    """BaseColumn is the super class for implementing Columns.

    Generally, you will only need to extend BaseColumn if you
    are implementing a new data provider.

    A Column represents a single time series of a symbol.

    Examples of commonly used time-series are adjusted_close,
    open, highh, low close, volume. However columns can also
    be used to represent fundamental time-series, or time-
    series from alternative sources.

    To implement a new type of Column, you must implement the
    'fetch' method.

    Example::

        class MyDataProvider(BaseColumn):

            def fetch(self, symbol):
                df = get_my_dataframe(symbol)
                return self.clean(df)

    Optionally, you may also need to perform additional cleaning
    of the data, you can do this by extending the clean() method.
    Don't forget to call super().clean(df).

    Example::

        class MyDataProvider(BaseColumn):

            def clean(self, df):
                df = df.rename(mapper={
                    'Open': 'open',
                    'High': 'high',
                    'Low': 'low',
                    'Close': 'close',
                }, axis='columns')

                return super().clean(df)

    When using an implementation of a subclass of BaseColumn, users are
    expected to at least specify the time_series that they want to access.

    Args:
        time_series (str): the name of the time_series that will be returned.
    """

    INITED = False

    def __init__(self, time_series: str, *args, **kwargs):  # noqa: D107
        self.time_series = time_series
        self._full_series = None
        self._series = None

    def get_label(self):
        """Return the label for this column."""
        return self.series.name

    def clone(self):
        """Return a new instance of oneself."""
        return self.__class__(self.time_series)

    def setup(self, symbol: str, env: dict = {}):
        """Setup the column.

        Called by the Symbol so that the symbol name can be passed.
        """
        self.symbol = symbol
        self.env = env

        # TODO File names should be managed in a central configuration
        data_cache = env.get('DATA_CACHE', os.environ.get('DATA_CACHE'))
        Path(data_cache).mkdir(parents=True, exist_ok=True)

        self.hdf5_file = os.path.join(
            data_cache, '{}.hdf5'.format(self.symbol))

    def clean(self, df):
        """Clean the data."""
        df = df.sort_index()
        # make tz aware if not already
        if not isinstance(df.index.dtype, pd.DatetimeTZDtype):
            df = df.tz_localize(pytz.UTC)

        return df

    def load_or_fetch_series(self, symbol: str):
        """Load of fetch the Dataframe, return the series.

        In order to return the time-series, first determine if we
        have it and can return it, or if we need to fetch it.

        TODO: Test for up-to-dateness (or maybe that happens in Symbol)?

        Args:
            symbol (str): the name of the symbol to fetch.

        Returns:
            pd.Series: time-series of the column
        """
        try:
            df = self.load(symbol)
        except (KeyError, FileNotFoundError):
            df = self.refresh()
        return df[self.time_series]

    def refresh(self):
        """Refresh the data from the source.

        Returns:
            pd.DataFrame: the whole dataframe (cleaned)
        """
        df = self.fetch(self.symbol)
        df = self.clean(df)
        self.save(df, self.symbol)
        return df

    def fetch(self, symbol: str):  # noqa: D102
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

    @property
    def series(self):
        """Get the data series as a pandas series.

        Returns:
            pd.Series: time series of the field
        """
        if self._full_series is None:
            self._full_series = self.load_or_fetch_series(self.symbol)
            self._series = self._full_series.copy()

        self.INITED = True
        return self._series

    def simulate(self, when):
        """Simulate a time ub history.

        Args:
            when (datetime): (optional) used when
                simulating historical data, typically
                using margot.backtest.
        """
        self._series = self._full_series[:when]

    @property
    def latest(self):
        """Return the latest value in this series."""
        return self.series.tail(1)[0]
