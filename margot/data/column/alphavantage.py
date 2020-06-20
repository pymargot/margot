import os
import logging
from alpha_vantage.timeseries import TimeSeries

from margot.data.column import BaseColumn

logger = logging.getLogger(__name__)

class Column(BaseColumn):
    """A single Symbol time series from AlphaVantage.

    Example::

        from margot.data.column import alphavantage as av

        volume = av.Column(time_series='adjusted_close')

    Args:
        time_series (str): the name of the time-series that will be returned
    """

    def clean(self, df):
        """Clean the df."""
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
        return super().clean(df)

    def fetch(self, symbol: str):
        """Fetch from remote - this could be the only service specific thing."""
        logger.info('fetching ({}) from alphavantage'.format(symbol))
        ts = TimeSeries(
            key=self.env.get(
                'ALPHAVANTAGE_API_KEY',
                os.environ.get('ALPHAVANTAGE_API_KEY')),
            output_format='pandas')
        df, metadata = ts.get_daily_adjusted(symbol, outputsize='full')
        return self.clean(df)
