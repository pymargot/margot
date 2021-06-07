import socket
import importlib
import inspect

from margot import BaseAlgo
from margot.config import settings


def send_message(msg):
    # post the signal to the manager... let him deal with it.
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(settings.sys.get('socket'))
        sock.sendall(msg.encode())
        sock.close()
        logger.info('Sent to manager.')
    except FileNotFoundError:
        logger.error('Unable to connect to server. Is it running?')
        raise OSError(
            'Unable to connect to {}'.format(
                settings.sys.get('socket')))


def init(algo_file, config, logger):
    logger.debug('initialising worker for {}'.format(algo_file))
    for name, cls in inspect.getmembers(
            importlib.import_module(algo_file),
            inspect.isclass):

        if issubclass(cls, BaseAlgo) and cls != BaseAlgo:
            logger.debug('Found algo {}'.format(cls))
            algo = cls()
            signal = algo.signal()
            logger.info('signal is: {}'.format(signal))
            message = 'SIGNAL {} | {} \n'.format(name, str(signal))
            send_message(message)
