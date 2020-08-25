from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# TODO move all this to a global config registry
LOCKFILE = '/tmp/.margot-lockfile'


def init(logger):
    if not Path(LOCKFILE).exists():
        scheduler = AsyncIOScheduler()
        scheduler.start()
        # We use a lockfile to prevent multiple servers running
        Path(LOCKFILE).touch()
        return scheduler
    else:
        logger.error('A manager is already running')
        raise Exception('A manager is already running')


def close(logger):
    logger.info('Shutting down the scheduler')
    Path(LOCKFILE).unlink()
