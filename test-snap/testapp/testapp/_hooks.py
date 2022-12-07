import logging

from snaphelpers import Snap

from ._log import setup_log


def install_hook(snap: Snap):
    logger = _get_logger(snap, "install")
    logger.info("hook called")


def configure_hook(snap: Snap):
    logger = _get_logger(snap, "configure")
    logger.info("hook called")


def _get_logger(snap: Snap, hook_name: str) -> logging.Logger:
    setup_log(snap.paths.common / "hooks.log")
    return logging.getLogger(f"hooks.{hook_name}")
