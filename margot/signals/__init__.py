
class Position(object):
    """Represents a Position with a symbol and a weight.

    Arguments:
        symbol (str): The identifier of the symbol. e.g. 'SPY'.
        weight (float): A value between -1.0 and +1.0 representing
            the weight of this symbol in the position list.
    """

    def __init__(self, symbol: str, weight: float, order_type: str):  # noqa: D107
        self.symbol = symbol
        self.weight = weight
        # TODO order_type should be checked.
        if self.weight > 1.0 or self.weight < -1.0:
            raise ValueError('weight must be a value between -1.0 and +1.0')

    def as_map(self):
        """Return the Position as a dictionary."""
        return {self.symbol: self.weight}

    def __repr__(self):
        """Represent."""
        return str((self.symbol, self.weight))
