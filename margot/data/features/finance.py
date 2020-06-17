import pandas as pd
import numpy as np

from margot.data.features import BaseFeature


class SimpleReturns(BaseFeature):
    """Simple returns are the percent change from yesterdays close to today's close.

    Args:
        column (str): The name of a price time series.
    """

    label = 'simple_returns'

    def feature(self, series):
        return series.pct_change().fillna(0)


class LogReturns(BaseFeature):
    """Log returns can be summed over time.

    Args:
        column (str): The name of the price time series.
    """

    label = 'log_returns'

    def feature(self, series):
        return np.log(1 + series.pct_change().fillna(0))


class RealisedVolatility(BaseFeature):
    """Realised volatility measures the variability of returns over a lookback window.

    Args:
        column (str): The name of a returns time series.
        window (int): Lookback window in trading days.

    Raises:
        AttributeError: A lookback window is required.
    """

    label = 'realised_vol'
    window = None

    def feature(self, series):
        if not self.window:
            raise AttributeError(
                'you must supply a lookback window for RealisedVolatility')
        return series.rolling(
            self.window).std() * np.sqrt(252)


class SimpleMovingAverage(BaseFeature):
    """Simple moving average of lookback window.

    Args:
        column (str): The name of a returns time series.
        window (int): Lookback window in trading days.
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
    """Upper bollinger band with window and standard deviation.

    Args:
        column (str): The name of a returns time series.
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
        column (str): The name of a returns time series.
        window (int): lookback in trading days. Defaults to 20
        width (float): width in standard deviations. Defaults to 2.0
    """

    window = 20
    width = 2.0
    label = 'lower_boll_band'

    def feature(self, series):
        return series.rolling(self.window).mean(
        ) - series.rolling(self.window).mean().std() * self.width
