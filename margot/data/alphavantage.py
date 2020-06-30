import os
import logging

from alpha_vantage.timeseries import TimeSeries

from margot.data.columns import BaseColumn, DailyMixin

logger = logging.getLogger(__name__)


class DailyAdjusted(BaseColumn, DailyMixin):
    """A daily time series from AlphaVantage.

    Example::

        from margot import alphavantage as av

        volume = av.DailyAdjusted(time_series='adjusted_close')

    Args:
        time_series (str): the name of the time-series that will be returned.
            Can be one of: 'open', 'high', 'low', 'close', 'adjusted_close',
            'volume', 'dividend_amount' or 'split_coefficient'.
    """

    def clean(self, df):
        """
        Clean the dataframe.

        Alphavantage has odd column names, so we'll fix those.
        """
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
        """
        Fetch from remote - this could be the only service specific thing.

        Args:
            symbol (str): the name of the symbol to fetch

        """
        logger.info('fetching ({}) from alphavantage'.format(symbol))
        ts = TimeSeries(
            key=os.environ.get('ALPHAVANTAGE_API_KEY'),
            output_format='pandas')
        df, _ = ts.get_daily_adjusted(symbol, outputsize='full')
        return self.clean(df)
