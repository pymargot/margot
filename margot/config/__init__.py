import os
from pathlib import Path
import logging
import configparser

from . import settings

CONFIG_FILE = "/etc/margot"

DEFAULT_CONFIG = """
[paths]
base_folder = .margot

[sys]
manager_python = /usr/bin/python3
socket = /tmp/.margot-socket
lockfile = /tmp/.margot-lockfile

[ibkr]
ib_port = 1234
ib_ip = 127.0.0.1
"""


def init():
    # logging
    logger = logging.getLogger("margot config")  # unless worker

    # load config
    cfg = configparser.ConfigParser()
    logger.info("loading config from {}".format(CONFIG_FILE))
    cfg.read(CONFIG_FILE)

    if not len(cfg.sections()):
        logger.warning("config not found at: {}.".format(CONFIG_FILE))
        logger.warning("Please create a config file /etc/margot")
        logger.warning("loading defaults")
        cfg.read_string(DEFAULT_CONFIG)

    for section in cfg.sections():
        setattr(settings, section, dict())
        for key, val in cfg.items(section):
            getattr(settings, section)[key] = val

    # find home folder
    base_folder = settings.paths.get("base_folder")
    home = Path.home().joinpath(base_folder)
    logger.debug("using margot_home {}".format(home))

    settings.paths = {
        "home": home,
        "algo_folder": home.joinpath("algos"),
        "log_folder": home.joinpath("logs"),
        "journal_folder": home.joinpath("journal"),
        "venv_folder": home.joinpath("venvs"),
        "cache": home.joinpath("cache"),
    }

    # create directory structure if it doesn't already exist.
    for folder in settings.paths.values():
        if not folder.exists():
            logger.info("creating new directory {}".format(folder))
            folder.mkdir()

    # look for algos
    algo_files = list(settings.paths["algo_folder"].glob("*.cfg"))
    logger.info(
        "found {} cfg files in {}".format(
            len(algo_files), settings.paths["algo_folder"]
        )
    )

    # create a dict to hold the algo configs (ConfigParser objects)
    settings.algos = dict()

    for algo_file in algo_files:
        logger.debug("parsing {}".format(algo_file))
        algo_config = configparser.ConfigParser()
        algo_config.read(algo_file)
        algo_name = algo_config.get("python", "file")

        settings.algos[algo_name] = dict()

        if len(algo_config.sections()):
            for section in algo_config.sections():
                settings.algos[algo_name][section] = dict()
                for key, val in algo_config.items(section):
                    settings.algos[algo_name][section][key] = val
        else:
            logger.warning("config not found at: {}.".format(CONFIG_FILE))
            return

    # lets collect up the os environment variables here too.
    if not hasattr(settings, "env"):
        settings.env = dict()

    for key in os.environ:
        settings.env[key] = os.environ[key]


if not settings.INITED:
    init()
