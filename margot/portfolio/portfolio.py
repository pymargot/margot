from math import sqrt
import configparser

from margot import BackTest
from margot.config import settings

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

    CONFIG_FILE = settings.paths.get('home').joinpath('portfolio.cfg')

    def __init__(self):  # noqa: D107
        # load config
        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.CONFIG_FILE)

    def calibrate(self, cls, algo_name, logger):
        bt = BackTest(algo=cls())
        rets = bt.run(periods=30)
        vol = rets.log_returns.std() * sqrt(252)
        self.cfg.set('margot_calculated', '{}.realised_vol'.format(algo_name), str(vol))
        
        self.cfg.write(self.CONFIG_FILE.open('w'))

        logger.info('Annualised vol at {}'.format(vol))
