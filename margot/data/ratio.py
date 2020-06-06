import pandas as pd


class Ratio(object):
    """Ratio of two series.

    Ratio = numerator / denomnator of two series.

    Args:
        numerator (str): the series to numerate the ratio
        denominator (str): the series to denominate the ratio
    """

    def __init__(self, numerator, denominator, **kwargs):
        self.numerator = numerator
        self.denominator = denominator
        self.__dict__.update(kwargs)
        self.series = None
        if not self.numerator and self.denominator:
            raise AttributeError("You must supply both a numerator and denominator")
        self.series = self.numerator.get_series() / self.denominator.get_series()

    def get_series(self):
        return self.series.rename('ratio_{}_{}'.format(self.numerator, self.denominator))
 