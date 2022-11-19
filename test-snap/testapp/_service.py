import logging
import time

from snaphelpers import Snap

from ._log import setup_log


class Service:
    """A no-op service."""

    def __init__(self, name):
        self.name = name

    def __call__(self, name):
        snap = Snap()
        setup_log(snap.paths.common / f"service-{name}.log")
        logging.info(f"Service {name} started")
        while True:
            logging.info(f"Service {name} still running")
            time.sleep(100)
