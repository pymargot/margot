#!/usr/bin/env python3

import sys
import argparse
import configparser
import logging

from ._version import get_versions

from margot import config # noqa this is to init the settings
from margot.config import settings

from margot.trade import manager, worker, backtest
from margot.trade.algos import load_algo


def main(args):
    
    # logging
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    logger = logging.getLogger('margot')

    if args.config:
        # reload config from new file
        settings.CONFIG_FILE = args.config
        config.init()

    if args.version: 
        print('margot version {}'.format(get_versions()['version']))
        return
    
    if args.backtest:
        backtest.init(args.backtest, settings, logger)

    elif args.worker:
        logger = logging.getLogger(args.worker)
        worker.init(args.worker, settings, logger)

    elif args.server:
        logger = logging.getLogger('margot')
        logger.info('starting margot manager (version {})'.format(get_versions()['version']))
        manager.init(settings, logger)

    else:
        print('--help for help.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='margot',
        description="Schedule and execute trading strategies with champagne and style.",
        epilog="As an alternative, params can be placed in a file, one per line, and specified as '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')

    parser.add_argument(
        "--version",
        help="Print margot version then exit.",
        action="store_true")
    
    parser.add_argument(
        "-v",
        "--verbose",
        help="Increase output verbosity for debugging",
        action="store_true")

    parser.add_argument(
        "-c",
        "--config",
        metavar="inifile",
        help="Specify a configuration file to use, instead of the default.",)
   
    parser.add_argument(
        "-b",
        "--backtest",
        metavar="algofile",
        help="Backtest an algorithm",)     
   
    parser.add_argument(
        "-w",
        "--worker",
        help="A worker runs an algorithm, usually invoked by the manager.",
        metavar="algofile",)  

    parser.add_argument(
        "-s",
        "--server",
        help="Server & manager eventloop. Schedules workers and manages trade execution.",
        action="store_true")      


    main(parser.parse_args())


