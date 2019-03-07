import logging


def install_hook(snap):
    _setup_log(snap.paths.common)
    logging.info('Install hook called')


def configure_hook(snap):
    _setup_log(snap.paths.common)
    logging.info('Configure hook called')


def _setup_log(common_dir):
    logfile = common_dir / 'hooks.log'
    logging.basicConfig(filename=str(logfile), level=logging.DEBUG)
