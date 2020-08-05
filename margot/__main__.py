#!/usr/bin/env python3

import sys
import argparse
import configparser
import logging

from ._version import get_versions

from margot import config # noqa this is to init the settings
from margot.config import settings

from margot.trade import manager, worker


def main(args):
    # version
    if args.version: 
        print('margot version {}'.format(get_versions()['version']))
        return
    
    # logging
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    if args.config:
        # reload config from new file
        settings.CONFIG_FILE = args.config
        settings.init()

    if args.worker:
        logger = logging.getLogger(args.worker)
        worker.init(args.worker, settings, logger)

    else:
        logger = logging.getLogger('margot')
        logger.info('starting margot (version {})'.format(get_versions()['version']))
        manager.init(settings, logger)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='margot',
        description="Schedule and execute trading strategies.",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')

    parser.add_argument(
        "-c",
        "--config",
        help="Specify a configuration file to use, instead of the default.",)

    parser.add_argument(
        "-w",
        "--worker",
        help="A worker runs an algorithm, usually invoked by the manager.",)    

    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity for debugging",
        action="store_true")

    parser.add_argument(
        "--version",
        help="Print margot version then exit.",
        action="store_true")

    main(parser.parse_args())


