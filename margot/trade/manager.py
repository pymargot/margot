from pathlib import Path
import asyncio

from .algos import load_algo
from . import scheduler, server
from margot.config import settings

def init(config, logger):
    logger.debug('initialising manager')
    # start the scheduler
    sched = scheduler.init(logger)
    # start the server to receive trading messages from algos
    server.init(logger)

    # look for algos
    algo_files = list(settings.paths['algo_folder'].glob('*.cfg'))
    logger.info('found {} cfg files in {}'.format(
        len(algo_files), 
        settings.paths['algo_folder']))

    for algo in algo_files:
        load_algo(algo, config, settings.paths, logger, sched)


    # load portfolio definition
    # eventloop
    # connect to brokers
    try:
        logger.info('running forever')
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.info('manager has been killed')
        scheduler.close(logger)
        pass
    except (Exception):
        logger.info('something went wrong - cleaning up lockfile')
        scheduler.close(logger)
        raise Exception
    