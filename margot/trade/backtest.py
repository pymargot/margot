from margot.config import settings
from margot.signals import BackTest

def init(algo_name, settings, logger):
    try:
        algo = settings.algos[algo_name]
    except KeyError:
        logger.error('Unable to locate config for algo {}'.format(algo_name))
        logger.error('Algos are: {}'.format(settings.algos.keys()))
        raise 
    
    logger.info('Backtesting {}'.format(algo_name))

    # the name of the algo should be registered in a registry - we know all about the algo from
    # the config. and the algo's thing - we need to get the algo config into live settings.

    bt = BackTest(algo=algo)
    rets = bt.walk_forward(start=START, end=END)


    # need to store the backtests for each algo so that we have volatility etc.
    