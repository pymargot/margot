import configparser
import subprocess

from margot.config import settings


def add_job(algo_config, venv, logger, sched, verbose=True):
    cmd = 'cd {} && {}/bin/python -m margot -v -w {}'.format(
        algo_config.get('python', 'working_dir'),
        venv,
        algo_config.get('python', 'algo')
    )

    logger.info('adding job: {}'.format(cmd))
    trigger = algo_config.get('schedule', 'trigger')

    if trigger == 'cron':
        return sched.add_job(
            subprocess.run,
            args=[cmd],
            kwargs={'shell': True},
            trigger = 'cron',
            day_of_week = algo_config.get('schedule', 'day_of_week'),
            hour = algo_config.getint('schedule', 'hour'),
            minute = algo_config.getint('schedule', 'minute'),
            second = algo_config.getint('schedule', 'second'),
            jitter = algo_config.getint('schedule', 'jitter')
        )

    if trigger == 'interval':
        return sched.add_job(
            subprocess.run,
            args=[cmd],
            kwargs={'shell': True},
            trigger = 'interval',
            minutes = algo_config.get('schedule', 'minutes'),
        )

def load_algo(algo, config, paths, logger, sched):
    """
    Load an algo from its cfg file.
    """
    logger.debug('parsing {}'.format(algo))
    algo_config = configparser.ConfigParser()
    algo_config.read(algo)
    try:
        algo_name = algo_config.get('algorithm', 'name')
        lang = algo_config.get('algorithm', 'lang')
        logger.info('algorithm, "{}" uses {}'.format(algo_name, lang))

        # does the venv exist?
        venv = settings.paths['venv_folder'].joinpath(algo_config.get('python', 'venv'))
        if not venv.exists():
            logger.info('creating venv {}'.format(venv))
            venv.mkdir()
            python3 = algo_config.get('python', 'interpreter', fallback='python3')
            logger.info(subprocess.run(
                '{} -m venv {}'.format(python3, venv),
                shell=True))
            
            # and install requirements
            for req, ver in algo_config.items('requirements'):
                logger.debug('installing requirement {} {}'.format(req, ver))
                logger.info(subprocess.run(
                    '{}/bin/pip install {} {}'.format(venv, req, ver),
                    shell=True))
        
        add_job(algo_config, venv, logger, sched)

    except configparser.NoOptionError as err:   
        logger.error('unable to load {}'.format(algo))
        logger.error(err)
        return
    # register algo in registry