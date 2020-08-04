from pathlib import Path

from .algos import load_algo

def init(config, logger):

    logger.debug('initialising manager')

    # find home folder
    base_folder = config.get('paths', 'base_folder')
    home = Path.home().joinpath(base_folder)
    logger.debug('using margot_home {}'.format(home))

    paths = {
        "algo_folder": home.joinpath('algos'),
        "log_folder": home.joinpath('logs'),
        "journal_folder": home.joinpath('journal'),
        "venv_folder": home.joinpath('venvs')
    }


    # create directory structure if it doesn't already exist.
    for folder in paths.values():
        if not folder.exists():
            logger.info('creating new directory {}'.format(folder))
            folder.mkdir()


    # look for algos
    algo_files = list(paths['algo_folder'].glob('*.cfg'))
    logger.info('found {} cfg files in {}'.format(len(algo_files), paths['algo_folder']))

    for algo in algo_files:
        load_algo(algo, config, paths, logger)


    # load portfolio definition
    # eventloop
    # connect to brokers

    