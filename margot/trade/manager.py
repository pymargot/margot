import asyncio

from .algos import load_algo
from . import scheduler, server
from margot.config import settings


def init(config, logger):
    try:
        # the scheduler runs algos on their schedule
        sched = scheduler.init(logger)

        # the server receives trading messages from algos
        server.init(logger)

        for algo in settings.algos.keys():
            load_algo(settings.algos[algo], logger, sched)
            # connect to brokers
            # load portfolio definition

        logger.info('running forever')
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.info('manager has been killed')
        scheduler.close(logger)
        pass
    except BaseException:
        logger.info('guru meditatiton - cleaning up lockfile')
        scheduler.close(logger)
        raise
