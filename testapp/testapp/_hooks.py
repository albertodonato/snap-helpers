import logging

from ._log import setup_log


def install_hook(snap):
    setup_log(snap.paths.common)
    logging.info('Install hook called')


def configure_hook(snap):
    setup_log(snap.paths.common)
    logging.info('Configure hook called')
