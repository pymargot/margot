import pandas as pd
import numpy as np

class BaseColumn(object):
    
    INITED = False

    def __init__(self, field, **kwargs):
        self.field = field
        self.__dict__.update(kwargs)
        self.series = None

    def get_series(self):
        return self.series


class SimpleReturns(BaseColumn):
    """Simple returns are the percent change from yesterday.

    Args:
        field (pd.Series): A price time series.
    """

    def _setup(self, base_series: pd.DataFrame):
        self.series = base_series.pct_change().fillna(0) / 100


class LogReturns(BaseColumn):
    """Log returns can be summed over time.

    Args:
        field (pd.Series): A price time series.
    """

    def _setup(self, base_series: pd.DataFrame):
        self.series = np.log(1 + base_series.pct_change().fillna(0)) / 100


class RealisedVolatility(BaseColumn):
    """Realised volatility measures the variability of returns over a lookback window.

    Args:
        field (pd.Series): A returns time series.
        window (int): Lookback window in trasing days.

    Raises:
        AttributeError: A lookback window is required.
    """

    window = None

    def _setup(self, base_series: pd.DataFrame):
        if not self.window:
            raise AttributeError('you must supply a lookback window for RealisedVolatility')
        self.series = base_series.multiply(100).rolling(self.window).std() * np.sqrt(252)