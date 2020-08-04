#!/usr/bin/env python3

import sys
import argparse
import configparser
import logging

from margot.trade import manager, worker

from ._version import get_versions

DEFAULT_CONFIG_FILE ='/etc/margot'

def main(args):
    # version
    if args.version: 
        print('margot version {}'.format(get_versions()['version']))
        return

    # logging
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    logger = logging.getLogger('margot') # unless worker
    logger.info('starting margot (version {})'.format(get_versions()['version']))

    # load config
    config_file = args.config if args.config else DEFAULT_CONFIG_FILE
    config = configparser.ConfigParser()
    logger.debug('loading config from {}'.format(config_file))
    config.read(config_file)
    if not config.sections():
        logger.info('config not found.')
        return

    if args.worker:
        worker.init(config, logger)
    else:
        manager.init(config, logger)


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


