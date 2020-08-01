from pathlib import Path
import configparser

def init(config, logger):

    logger.debug('initialising daemon')

    # find home folder
    base_folder = config.get('paths', 'base_folder')
    home = Path.home().joinpath(base_folder)
    logger.debug('using margot_home {}'.format(home))

    algo_folder = home.joinpath('algos')
    log_folder = home.joinpath('logs')
    journal_folder = home.joinpath('journal')

    for folder in [home, algo_folder, log_folder, journal_folder]:
        if not folder.exists():
            logger.info('creating new directory {}'.format(folder))
            folder.mkdir()

    # load any algos
    algo_files = list(algo_folder.glob('*.cfg'))
    logger.info('found {} cfg files in {}'.format(len(algo_files), algo_folder))

    for algo in algo_files:
        logger.debug('using {}'.format(algo))
        algo_config = configparser.ConfigParser()
        algo_config.read(algo)
        try:
            algo_name = algo_config.get('algorithm', 'name')
            algo_subdir = algo_config.get('algorithm', 'subdir')
            logger.info('found algorithm, "{}" in directory {}'.format(algo_name, algo_subdir))
        except configparser.NoOptionError as err:   
            logger.error('unable to load {}'.format(algo))
            logger.error(err)
            return
        # register algo in registry

    # load portfolio definition
    # eventloop
    # connect to brokers

    