import pandas as pd
import numpy as np

from margot.data.column import BaseColumn

class BaseFeature(object):

    INITED = False

    def get_label(self):
        try:
            return self.feature_name
        except AttributeError:
            raise AttributeError(
                'Please declare a label attribute for this feature')

    def __init__(self, column: BaseColumn, **kwargs):
        self.column = column
        self.__dict__.update(kwargs)
        self.series = None

    def get_series(self):
        if self.series is None:
            series = self.feature(self.column.get_series())
            self.series = series.rename(self.get_label())
        return self.series

    def get_label(self):
        return self.label

    def feature(self, series: pd.Series):
        raise NotImplementedError("please implement the feature")


class SimpleReturns(BaseFeature):
    """Simple returns are the percent change from yesterdays close to today's close.

    Args:
        column (pd.Series): A price time series.
    """
    label = 'simple_returns'

    def feature(self, series):
        return series.pct_change().fillna(0) / 100


class LogReturns(BaseFeature):
    """Log returns can be summed over time.

    Args:
        field (pd.Series): A price time series.
    """
    label = 'log_returns'

    def feature(self, series):
        return np.log(1 + series.pct_change().fillna(0)) / 100


class RealisedVolatility(BaseFeature):
    """Realised volatility measures the variability of returns over a lookback window.

    Args:
        field (pd.Series): A returns time series.
        window (int): Lookback window in trasing days.

    Raises:
        AttributeError: A lookback window is required.
    """

    label = 'realised_vol'
    window = None

    def feature(self, series):
        if not self.window:
            raise AttributeError(
                'you must supply a lookback window for RealisedVolatility')
        return series.multiply(100).rolling(
            self.window).std() * np.sqrt(252)


class SimpleMovingAverage(BaseFeature):
    """Simple moving average of lookback, window.

    Args:
        BaseColumn ([type]): [description]
    """

    window = None

    def get_label(self):
        return 'sma{}'.format(self.window)

    def feature(self, series):
        if not self.window:
            raise AttributeError(
                'you must supply a lookback window for SimpleMovingAverage')
        return series.rolling(self.window).mean()


class UpperBollingerBand(BaseFeature):
    """Upper bollinger band of window and standard deviation.

    Args:
        window (int): lookback in trading days. Defaults to 20
        width (float): width in standard deviations. Defaults to 2.0
    """

    window = 20
    width = 2.0
    label = 'upper_boll_band'

    def feature(self, series):
        return series.rolling(self.window).mean(
        ) + series.rolling(self.window).mean().std() * self.width


class LowerBollingerBand(BaseFeature):
    """Lower bollinger band of window and standard deviation.

    Args:
        window (int): lookback in trading days. Defaults to 20
        width (float): width in standard deviations. Defaults to 2.0
    """

    window = 20
    width = 2.0
    label = 'lower_boll_band'

    def feature(self, series):
        return series.rolling(self.window).mean(
        ) - series.rolling(self.window).mean().std() * self.width
