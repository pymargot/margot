import configparser
import subprocess

from margot.config import settings


def add_job(algo, logger, sched, verbose=True):
    cmd = 'cd {} && {}/bin/python -m margot -v -w {}'.format(
        algo['python']['working_dir'],
        algo['venv'],
        algo['python']['file']
    )

    logger.info('adding job: {}'.format(cmd))
    trigger = algo['schedule']['trigger']

    if trigger == 'cron':
        return sched.add_job(
            subprocess.run,
            args=[cmd],
            kwargs={'shell': True},
            trigger='cron',
            day_of_week=algo['schedule'].get('day_of_week'),
            hour=algo['schedule'].get('hour'),
            minute=algo['schedule'].get('minute'),
            second=algo['schedule'].get('second'),
            jitter=int(algo['schedule'].get('jitter'))
        )

    if trigger == 'interval':
        return sched.add_job(
            subprocess.run,
            args=[cmd],
            kwargs={'shell': True},
            trigger='interval',
            minutes=algo['schedule'].get('minutes'),
        )


def load_algo(algo, logger, sched):
    """
    Load an algo from its cfg file.
    """

    # does the venv exist?
    algo['venv'] = settings.paths['venv_folder'].joinpath(
        algo['python']['venv'])

    if not algo['venv'].exists():
        logger.info('creating venv {}'.format(algo['venv']))
        algo['venv'].mkdir()
        python3 = algo['python'].get('interpreter', 'python3')
        logger.info(subprocess.run(
            '{} -m venv {}'.format(python3, algo['venv']),
            shell=True))

        # and install requirements
        for req, ver in algo['requirements'].items():
            logger.debug('installing requirement {} {}'.format(req, ver))
            logger.info(subprocess.run(
                '{}/bin/pip install {} {}'.format(algo['venv'], req, ver),
                shell=True))

    add_job(algo, logger, sched)

    # register algo in registry
