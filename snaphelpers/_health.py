import re
from typing import Optional

from ._ctl import (
    SnapCtl,
    SnapHealthStatus,
)

# Valid format for the status code
STATUS_CODE_RE = re.compile(r"^[a-z](?:-?[a-z0-9])+$")


class SnapHealth:
    """Snap health.

    This provides an interfaces for setting health for the snap.

    """

    def __init__(self, snapctl: Optional[SnapCtl] = None):
        self._snapctl = snapctl or SnapCtl()

    def okay(self):
        """Set the status of the snap to "okay"."""
        self._snapctl.set_health(SnapHealthStatus.OKAY)

    def waiting(self, message: str, code: Optional[str] = None):
        """Set the status of the snap to "waiting".

        :param message: a message string for the status
        :param code: an optional code string
        """
        self._set_health(SnapHealthStatus.WAITING, message, code)

    def blocked(self, message: str, code: Optional[str] = None):
        """Set the status of the snap to "blocked".

        :param message: a message string for the status
        :param code: an optional code string
        """
        self._set_health(SnapHealthStatus.BLOCKED, message, code)

    def error(self, message: str, code: Optional[str] = None):
        """Set the status of the snap to "error".

        :param message: a message string for the status
        :param code: an optional code string
        """
        self._set_health(SnapHealthStatus.ERROR, message, code)

    def _set_health(self, status: SnapHealthStatus, message: str, code: Optional[str]):
        if not message:
            raise ValueError("Health status message must not be empty")
        if code is not None and not STATUS_CODE_RE.match(code):
            raise ValueError("Invalid health status code format")
        self._snapctl.set_health(status, message=message, code=code)
