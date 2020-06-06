import pandas as pd
import numpy as np


class BaseFeature(object):

    INITED = False

    def get_feature_name(self):
        try:
            return self.feature_name
        except AttributeError:
            raise AttributeError(
                'Please declare a feature_name attribute for this feature')

    def __init__(self, column, **kwargs):
        self.column = column
        self.__dict__.update(kwargs)
        self.series = None

    def get_series(self):
        return self.series.rename(self.get_feature_name())

    def get_label(self):
        return self.feature_name


class SimpleReturns(BaseFeature):
    """Simple returns are the percent change from yesterdays close to today's close.

    Args:
        column (pd.Series): A price time series.
    """
    feature_name = 'simple_returns'

    def _setup(self, base_series: pd.DataFrame):
        self.series = base_series.pct_change().fillna(0) / 100


class LogReturns(BaseFeature):
    """Log returns can be summed over time.

    Args:
        field (pd.Series): A price time series.
    """
    feature_name = 'log_returns'

    def _setup(self, base_series: pd.DataFrame):
        self.series = np.log(1 + base_series.pct_change().fillna(0)) / 100


class RealisedVolatility(BaseFeature):
    """Realised volatility measures the variability of returns over a lookback window.

    Args:
        field (pd.Series): A returns time series.
        window (int): Lookback window in trasing days.

    Raises:
        AttributeError: A lookback window is required.
    """

    feature_name = 'realised_vol'
    window = None

    def _setup(self, base_series: pd.DataFrame):
        if not self.window:
            raise AttributeError(
                'you must supply a lookback window for RealisedVolatility')
        self.series = base_series.multiply(100).rolling(
            self.window).std() * np.sqrt(252)


class SimpleMovingAverage(BaseFeature):
    """Simple moving average of lookback, window.

    Args:
        BaseColumn ([type]): [description]
    """

    window = None

    def get_feature_name(self):
        return 'sma{}'.format(self.window)

    def _setup(self, base_series: pd.DataFrame):
        if not self.window:
            raise AttributeError(
                'you must supply a lookback window for SimpleMovingAverage')
        self.series = base_series.rolling(self.window).mean()


class UpperBollingerBand(BaseFeature):
    """Upper bollinger band of window and standard deviation.

    Args:
        window (int): lookback in trading days. Defaults to 20
        width (float): width in standard deviations. Defaults to 2.0
    """

    window = 20
    width = 2.0
    feature_name = 'upper_boll_band'

    def _setup(self, base_series: pd.DataFrame):
        self.series = base_series.rolling(self.window).mean(
        ) + base_series.rolling(self.window).mean().std() * self.width


class LowerBollingerBand(BaseFeature):
    """Lower bollinger band of window and standard deviation.

    Args:
        window (int): lookback in trading days. Defaults to 20
        width (float): width in standard deviations. Defaults to 2.0
    """

    window = 20
    width = 2.0
    feature_name = 'lower_boll_band'

    def _setup(self, base_series: pd.DataFrame):
        self.series = base_series.rolling(self.window).mean(
        ) - base_series.rolling(self.window).mean().std() * self.width




