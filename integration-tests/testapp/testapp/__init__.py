from datetime import datetime

from snaphelpers import Snap


def log_message(snap: Snap, hook_name: str):
    logfile = snap.paths.common / hook_name
    with logfile.open("a") as fd:
        timestamp = datetime.now().strftime("%Y-%m-%d|%H:%M:%s")
        fd.write(f"{timestamp} - {hook_name} called\n")


def install_hook(snap: Snap):
    log_message(snap, "install")


def configure_hook(snap: Snap):
    log_message(snap, "configure")
