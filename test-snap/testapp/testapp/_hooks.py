import logging

from ._log import setup_log


def install_hook(snap):
    setup_log(snap.paths.common / "hooks.log")
    logging.info("Hook called: install")


def configure_hook(snap):
    setup_log(snap.paths.common / "hooks.log")
    logging.info("Hook called: configure")
