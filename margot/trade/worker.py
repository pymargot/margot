from pathlib import Path
import importlib, inspect
import configparser

from margot import BaseAlgo


def init(worker, config, logger):
    logger.debug('initialising worker for {}'.format(worker))
    for name, cls in inspect.getmembers(
            importlib.import_module(worker), 
            inspect.isclass):

        if issubclass(cls, BaseAlgo) and cls != BaseAlgo:
            logger.debug('{} - {}'.format(name, name))
            # load the class
            # run the algo
            # post the signal to the manager... let him deal with it.
