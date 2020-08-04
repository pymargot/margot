from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler

LOCKFILE = '/tmp/.margot'

def init(logger):
    if not Path(LOCKFILE).exists():
        scheduler = AsyncIOScheduler()
        scheduler.start()
        Path(LOCKFILE).touch()
        return scheduler
    else:
        logger.error('A manager is already running')
        raise Exception('A manager is already running')

def close(logger):
    logger.info('Shutting down the scheduler')
    Path(LOCKFILE).unlink()