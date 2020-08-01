#!/usr/bin/env python3

import sys
import argparse
import configparser
import logging

from margot.trade import daemon

from ._version import get_versions

DEFAULT_CONFIG_FILE ='/etc/margot'

def main(args):
    # version
    if args.version: 
        print('margot version {}'.format(get_versions()['version']))
        return

    # logging
    loglevel = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    logger = logging.getLogger('margot')
    logger.info('starting margot (version {})'.format(get_versions()['version']))

    # load config
    config_file = args.config if args.config else DEFAULT_CONFIG_FILE
    config = configparser.ConfigParser()
    logger.debug('loading config from {}'.format(config_file))
    config.read(config_file)
    if not config.sections():
        logger.info('config not found.')
        return

    daemon.init(config, logger)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='margot',
        description="Makes the complex simple",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')

    parser.add_argument(
        "-c",
        "--config",
        help="Specify a configuration file to use, instead of the default.",)

    parser.add_argument(
        "-d",
        "--debug",
        help="increase output verbosity for debugging",
        action="store_true")

    parser.add_argument(
        "-v",
        "--version",
        help="Print margot version then exit.",
        action="store_true")

    # parser.add_argument(
    #     "-i",
    #     "--info",
    #     help="Print lots of useful information. Versions, configuration and state",
    #     action="store_true")

    # parser.add_argument(
    #     "-t",
    #     "--test",
    #     help="Don’t run, just test the configuration file. Checks configuration for correct syntax and then try to open files referred in configuration.",
    #     action="store_true")

    main(parser.parse_args())


