from margot import BackTest


class Strategy(object):
    """
    A trading Strategy.

    Represents a backtested algo, with a recent realised volatility
    and a target volatility for postfolio sizing.

    Args:
        object (BaseAlgo): A margot algrithm.
        recent_vol (float): Recent measured volatility.
        target_vol (float): Target volatility for portfolio contribution.
    """

    def __init__(self, algo, recent_vol, target_vol):   # noqa: D107
        self.algo = algo
        self.recent_vol = recent_vol
        self.target_vol = target_vol

    def vol_size(self):
        return self.recent_vol / self.target_vol


class Portfolio(object):
    """
    A Porfolio of trading Strategies.

    Represents a portfolio of algorithms, each with a measured recent volatility
    and a target volatility. The portfolio has an account size and a target
    volatility for the portfolio as a whole.

    Args:
        object (BaseAlgo): A margot algrithm.
        account_size (int): In dollars, the size of the account.
        target_vol (float): Target volatility for the portfolio as a whole.
    """

    def __init__(self, account_size, target_vol):  # noqa: D107
        self.account_size = account_size
        self.target_vol = target_vol
        self.strategies = list()

    def add_strategy(self, algo, target_vol):
        """Add a strategy to the portfolio.

        Args:
            algo (Algo): A Margot Trading Algorithm
            target_vol (float): the vol were aiming for
        """
        bt = BackTest(algo)

        # TODO: periods assumes we're looking at days.
        bt.run(periods=30)

        self.strategies.append(
            Strategy(algo, bt.volatility(), target_vol)
        )
