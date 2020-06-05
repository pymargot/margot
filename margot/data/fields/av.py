import pandas as pd
import pytz
from alpha_vantage.timeseries import TimeSeries

from margot.data.fields import BaseField


class Field(BaseField):
    """A single Symbol time series from AlphaVantage.

    Example: 
        volume = fields.AlphaVantage(function='historical_daily_adjusted', field='volume')

    Args:
        function (str): the name of the function passed to the Alphavantage API
        field (str): the name of the column that will be returned
    """

    def _update(self):
        ts = TimeSeries(key=self.env.get('ALPHAVANTAGE_API_KEY'), output_format='pandas')
        self.data, self.metadata = ts.get_daily_adjusted(self.symbol, outputsize='full')
        self.data = self.data.sort_index()

        # Ensure the index is TZ aware.
        self.data = self.data.tz_localize(pytz.UTC)

        # Standardise the column names
        self.data = self.data.rename(mapper={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. adjusted close': 'adjusted_close',
            '6. volume': 'volume',
            '7. dividend amount': 'divident_amount',
            '8. split coefficient': 'split_coefficient'
        }, axis='features')
        self.save()

    def _load_or_update_series(self):
        """[summary]

        Returns:
            pd.Series: time series of the field
        """
        try:
            self.load()
        except FileNotFoundError:
            self._update()

        return self.data[self.field]

