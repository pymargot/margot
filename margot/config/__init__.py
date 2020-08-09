from pathlib import Path
import logging
import configparser

from . import settings

CONFIG_FILE ='/etc/margot'

def init():
    # logging
    logger = logging.getLogger('margot config') # unless worker
    
    # load config
    config = configparser.ConfigParser()
    logger.debug('loading config from {}'.format(CONFIG_FILE))
    config.read(CONFIG_FILE)

    if len(config.sections()):
        for section in config.sections():
            for key, val in config.items(section):
                setattr(settings, key, val)
    else:       
        logger.warning('config not found at: {}.'.format(CONFIG_FILE))
        return

    # find home folder
    base_folder = config.get('paths', 'base_folder')
    home = Path.home().joinpath(base_folder)
    logger.debug('using margot_home {}'.format(home))

    settings.paths = {
        "algo_folder": home.joinpath('algos'),
        "log_folder": home.joinpath('logs'),
        "journal_folder": home.joinpath('journal'),
        "venv_folder": home.joinpath('venvs'),
        "cache": home.joinpath('cache')
    }

    # create directory structure if it doesn't already exist.
    for folder in settings.paths.values():
        if not folder.exists():
            logger.info('creating new directory {}'.format(folder))
            folder.mkdir()
    

if not settings.INITED: 
    init()
