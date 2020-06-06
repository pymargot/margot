import pandas as pd


class Ratio(object):
    """Ratio of two series.

    Ratio = numerator / denomnator of two series.

    Args:
        numerator (str): the series to numerate the ratio
        denominator (str): the series to denominate the ratio
        label (str): give it a name for your dataframe. e.g. current_ratio
    """

    def __init__(self, numerator, denominator, label, **kwargs):
        self.numerator = numerator
        self.denominator = denominator
        self.__dict__.update(kwargs)
        self.series = None
        self.label = label
        if not self.numerator and self.denominator:
            raise AttributeError("You must supply both a numerator and denominator")
        self.series = self.numerator.get_series() / self.denominator.get_series()

    def get_series(self):
        return self.series.rename(self.label)

    def to_pandas(self):
        return self.get_series().to_frame()
 