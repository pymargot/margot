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
        self._series = None
        self.base_column = None

    def clone(self):
        """Return a new instance of oneself."""
        return self.__class__(self.column, *self.args, **self.kwargs)

    def set_column(self, base_column: BaseColumn):
        self.base_column = base_column

    def get_column_name(self) -> str:
        return self.column

    @property
    def series(self):
        if self._series is None:
            # TODO - consider set_column - used after cloning.
            series = self.feature(self.base_column.series)
            self._series = series.rename(self.get_label())
        return self._series

    @series.setter
    def set_series(self, series):
        self._series = series

    def get_label(self):
        """Return the label for this feature.

        Override this to customise.

        Returns:
            str: the label to be used in the pandas column.
        """
        return self.label

    def feature(self, series: pd.Series):  # noqa: D102
        raise NotImplementedError("please implement the feature")

    def simulate(self, when):
        """Recalculate the feature, typically in a simulation."""
        self._series = None
        self._series = self.series[:when]

    @property
    def latest(self):
        """Return the latest value in this series."""
        return self.series.tail(1)[0]
