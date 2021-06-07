import socket
import json

from math import sqrt

from margot.config import settings
from margot import BaseAlgo
from margot.portfolio import Portfolio

import importlib
import inspect


def ipc_request(msg, logger):
    # requst the manager for something
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(settings.sys.get('socket'))
        sock.sendall(msg.encode())
        logger.debug('Message sent: {}'.format(msg))
        data = sock.recv(4096)
        sock.close()
        reply = data.decode()
        logger.debug('Received {}'.format(reply))
        return json.loads(reply)

    except FileNotFoundError:
        logger.error('Unable to connect to server. Is it running?')
        raise OSError(
            'Unable to connect to {}'.format(
                settings.sys.get('socket')))


def init(algo_name, settings, logger):
    algo = ipc_request('GETALGO {} \n'.format(algo_name), logger)
    logger.info('Inspecting {}'.format(algo.get('algorithm').get('name')))

    for name, cls in inspect.getmembers(
            importlib.import_module(algo.get('python').get('file')),
            inspect.isclass):
        logger.debug('Inspecting {}'.format(cls))
        if issubclass(cls, BaseAlgo) and cls != BaseAlgo:
            logger.info('Found algo class {}'.format(cls))
            pf = Portfolio()
            pf.calibrate(cls, algo_name, logger)

    # need to store the backtests for each algo so that we have volatility etc.
