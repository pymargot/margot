import os
from alpha_vantage.timeseries import TimeSeries

from margot.data.column import BaseColumn


class Column(BaseColumn):
    """A single Symbol time series from AlphaVantage.

    Example:
        volume = column.AlphaVantage(function='historical_daily_adjusted', field='volume')

    Args:
        function (str): the name of the function passed to the Alphavantage API
        column (str): the name of the column that will be returned
    """

    def fetch(self, symbol: str):
        """Fetch from remote - this could be the only service specific thing."""
        print('fetching {}'.format(symbol))
        ts = TimeSeries(
            key=self.env.get(
                'ALPHAVANTAGE_API_KEY',
                os.environ.get('ALPHAVANTAGE_API_KEY')),
            output_format='pandas')
        df, metadata = ts.get_daily_adjusted(symbol, outputsize='full')
        return self.clean(df)
