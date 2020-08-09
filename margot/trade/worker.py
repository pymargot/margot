import socket
from pathlib import Path
import importlib, inspect
import configparser

from margot import BaseAlgo
from margot.config import settings


def init(worker, config, logger):
    logger.debug('initialising worker for {}'.format(worker))
    for name, cls in inspect.getmembers(
            importlib.import_module(worker), 
            inspect.isclass):

        if issubclass(cls, BaseAlgo) and cls != BaseAlgo:
            logger.debug('Found algo {}'.format(cls))
            algo = cls()
            signal = algo.signal()
            logger.info('signal is: {}'.format(signal))
            message = '{} | {}'.format(name, str(signal))
            # post the signal to the manager... let him deal with it.
            try:
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.connect(settings.socket)
                sock.sendall(message.encode())
                sock.close()
                logger.info('Sent to manager.')
            except FileNotFoundError:
                logger.error('Unable to connect to server. Is it running?')
                raise OSError('Unable to connect to {}'.format(settings.socket))