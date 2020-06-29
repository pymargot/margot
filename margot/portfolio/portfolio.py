from margot import BackTest


class Strategy(object):
 
    def __init__ (self, algo, recent_vol, target_vol):   # noqa: D107
        self.algo = algo
        self.recent_vol = recent_vol
        self.target_vol = target_vol

    def vol_size(self):
        return self.recent_vol / self.target_vol


class Portfolio(object):

    def __init__ (self, account_size, target_vol):  # noqa: D107
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

        #TODO: periods assumes we're looking at days.
        bt.run(periods=30)  

        self.strategies.append(
            Strategy(algo, bt.volatility(), target_vol)
            )
        