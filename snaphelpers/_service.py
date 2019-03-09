from typing import (
    Dict,
    Optional,
)

from ._ctl import (
    ServiceInfo,
    SnapCtl,
)


class SnapService:
    """A service defined in the Snap."""

    def __init__(self, info: ServiceInfo, snapctl: Optional[SnapCtl] = None):
        self._info = info
        self._snapctl = snapctl or SnapCtl()

    def __getattr__(self, attr):
        # forward attributes defined in ServiceInfo
        return getattr(self._info, attr)

    def __eq__(self, other) -> bool:
        return self._info == other._info and self._snapctl is other._snapctl

    def start(self, enable: bool = False):
        """Start the service.

        :param enable: whether to also enable the service at startup.

        """
        self._snapctl.start(self.name, enable=enable)
        self.refresh_status()

    def stop(self, disable: bool = False):
        """Stop the service.

        :param disable: whether to also disable the service at startup.

        """
        self._snapctl.stop(self.name, disable=disable)
        self.refresh_status()

    def restart(self, reload: bool = False):
        """Restart the service.

        :param reload: whether to reload the service if supported.

        """
        self._snapctl.restart(self.name, reload=reload)
        self.refresh_status()

    def refresh_status(self):
        """Update the status of the ervice service."""
        [self._info] = self._snapctl.services(self.name)


class SnapServices:
    """Manage services in the snap."""

    def __init__(self, snapctl: Optional[SnapCtl] = None):
        self._snapctl = snapctl or SnapCtl()

    def list(self) -> Dict[str, SnapService]:
        """Return services by name."""
        return {
            info.name: SnapService(info, snapctl=self._snapctl)
            for info in self._snapctl.services()
        }

    def start(self, enable: bool = False):
        """Start all services.

        :param enable: whether to also enable services at startup.

        """
        self._snapctl.start(enable=enable)

    def stop(self, disable: bool = False):
        """Stop all services.

        :param disable: whether to also disable services at startup.

        """
        self._snapctl.stop(disable=disable)

    def restart(self, reload: bool = False):
        """Restart all services.

        :param reload: whether to reload services if supported.

        """
        self._snapctl.restart(reload=reload)
