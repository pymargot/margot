import pandas as pd


class Ratio(object):
    """Ratio of two series.

    Ratio = numerator / denominator of two time-series.

    Example::

        my_ratio = Ratio(numerator=symbol_1.adj_close,
                         denominator=symbol_2.adj_close,
                         label='s1_s2_ratio')

    Args:
        numerator (str): the series to numerate the ratio
        denominator (str): the series to denominate the ratio
        label (str): give it a name for your dataframe. e.g. current_ratio
    """

    def __init__(self, numerator, denominator, label, **kwargs):    # noqa: D107
        self.numerator = numerator
        self.denominator = denominator
        self._series = None
        self.label = label
        self.__dict__.update(kwargs)

        if not self.numerator and self.denominator:
            raise AttributeError(
                "You must supply both a numerator and denominator")

        self.series = self.make_series()

    def make_series(self):
        return self.numerator.series.divide(self.denominator.series)

    @property
    def series(self):
        return self._series.rename(self.label)

    @series.setter
    def series(self, series):
        self._series = series

    def to_pandas(self):
        return self.series.to_frame()

    def simulate(self, when=None):
        self.series = self.make_series()[:when]

    @property
    def latest(self):
        """Return the latest value in this series"""
        return self.series.tail(1)[0]
