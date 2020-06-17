import pandas as pd

from margot.data.column import BaseColumn


class BaseFeature(object):

    INITED = False

    def get_label(self):
        try:
            return self.label
        except AttributeError:
            raise AttributeError(
                'Please declare a label attribute for this feature')

    def __init__(self, column: str, *args, **kwargs):  # noqa: D107
        self.column = column
        self.__dict__.update(kwargs)
        self.kwargs = kwargs
        self.args = args
        self.series = None
        self.base_column = None

    def clone(self):
        """Return a new instance of oneself."""
        return self.__class__(self.column, *self.args, **self.kwargs)

    def set_column(self, base_column: BaseColumn):
        self.base_column = base_column

    def get_column_name(self) -> str:
        return self.column

    def get_series(self):
        if self.series is None:
            # TODO - consider set_column - used after cloning.
            series = self.feature(self.base_column.get_series())
            self.series = series.rename(self.get_label())
        return self.series

    def get_label(self):
        return self.label

    def feature(self, series: pd.Series):
        raise NotImplementedError("please implement the feature")

    @property
    def latest(self):
        """Return the latest value in this series"""
        return self.get_series().tail(1)[0]