import os
import logging

import pandas as pd

from margot.data.column import BaseColumn

logger = logging.getLogger(__name__)


class Column(BaseColumn):
    """A single OHLC timeiseries from CBOE.

    Currently supports the symbols, 'VIX' and 'VIX3M'.

    Collects the time-series: open, high, low, close.

    Example::

        from margot.data.column import cboe

        open = cboe.Column(time_series='open')
        close = cboe.Column(time_series='close')

    Args:
        column (str): the name of the column that will be returned
    """

    INDEX = {
        'VIX': {
            'url': 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vixcurrent.csv',
            'skiprows': 1,
            'index_col': 0
        },

        'VIX3M': {
            'url': 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vix3mdailyprices.csv',
            'skiprows': 2,
            'index_col': 0
        }
    }

    def clean(self, df):
        """Additional cleaning for CBOE symbols."""
        df = df.rename(mapper={
            'VIX Open': 'open',
            'VIX High': 'high',
            'VIX Low': 'low',
            'VIX Close': 'close',
            'OPEN': 'open',
            'HIGH': 'high',
            'LOW': 'low',
            'CLOSE': 'close'
        }, axis='columns')

        return super().clean(df)

    def fetch(self, symbol: str):
        """Fetch from remote - this could be the only service specific thing."""
        logger.info('fetching ({}) from cboe'.format(symbol))

        try:
            df = pd.read_csv(self.INDEX[symbol].get('url'),
                             skiprows=self.INDEX[symbol].get('skiprows'),
                             index_col=self.INDEX[symbol].get('index_col'),
                             parse_dates=True)
        except KeyError:
            raise KeyError('The CBOE fetcher doesn\'t know about that symbol.')

        return self.clean(df)
