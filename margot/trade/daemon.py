from pathlib import Path

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
    algo_files = list(algo_folder.glob('**/*.py'))
    logger.info('found {} algos in {}'.format(len(algo_files), algo_folder))

    # load portfolio definition
    # eventloop
    # connect to brokers

    