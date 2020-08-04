import configparser
import subprocess


def load_algo(algo, config, paths, logger):
        logger.debug('parsing {}'.format(algo))
        algo_config = configparser.ConfigParser()
        algo_config.read(algo)
        try:
            algo_name = algo_config.get('algorithm', 'name')
            lang = algo_config.get('algorithm', 'lang')
            logger.info('algorithm, "{}" uses {}'.format(algo_name, lang))

            # does the venv exist?
            venv = paths['venv_folder'].joinpath(algo_config.get('python', 'venv'))
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

        except configparser.NoOptionError as err:   
            logger.error('unable to load {}'.format(algo))
            logger.error(err)
            return
        # register algo in registry