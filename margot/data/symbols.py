from inspect import getmembers

from margot.data.fields import BaseField
from margot.data.features import BaseColumn


class Symbol(object):
    """A Symbol, that has fields and features.

    Args:
        object ([type]): [description]

    Raises:
        NotImplementedError: [description]

    Returns:
        [type]: [description]
    """

    def __init__(self, symbol: str, env: dict = {}):
        """Initiate."""
        self.symbol = symbol
        self.env = env
        self.fields = [
            member for member,
            ref in getmembers(self) if isinstance(
                ref,
                BaseField)]
        self.features = [
            member for member,
            ref in getmembers(self) if isinstance(
                ref,
                BaseColumn)]

        for field in self.fields:
            getattr(self, field)._setup(symbol=self.symbol, env=self.env)

        for column in self.features:
            field_name = getattr(self, column).field
            base_series = getattr(self, field_name).get_series()
            getattr(self, column)._setup(base_series=base_series)
