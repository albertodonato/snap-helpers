from typing import (
    Any,
    cast,
    Mapping,
    Optional,
)

from ._conf import SnapConfig
from ._ctl import SnapCtl
from ._env import SnapEnviron
from ._health import SnapHealth
from ._meta import SnapMetadataFiles
from ._path import SnapPaths
from ._service import SnapServices


class EnvironProperty:
    """Wrapper to get properties from a :class:`SnapEnviron` instance."""

    def __init__(self, name: str):
        self.name = name

    def __get__(self, instance: "Snap", owner: Any) -> str:
        return cast(str, getattr(instance.environ, self.name))


class Snap:
    """Top-level wrapper for a Snap."""

    #: Access to snap configuration
    config: SnapConfig
    #: Access to snap environment variables
    environ: SnapEnviron
    #: Access to snap health status
    health: SnapHealth
    #: Access to snap-specific paths
    paths: SnapPaths
    #: Access to snap services
    services: SnapServices
    #: Access to snap metadata files
    metadata_files: SnapMetadataFiles

    #: The snap name
    name = EnvironProperty("NAME")
    #: The snap instance name (usually same as the ``name``, unless parallel
    # installs are used)
    instance_name = EnvironProperty("INSTANCE_NAME")
    #: The snap version
    version = EnvironProperty("VERSION")
    #: The snap revision
    revision = EnvironProperty("REVISION")

    def __init__(self, environ: Optional[Mapping[str, str]] = None):
        self.environ = SnapEnviron(environ=environ)
        self.paths = SnapPaths(env=self.environ)
        snapctl = SnapCtl(env=self.environ)
        self.config = SnapConfig(snapctl=snapctl)
        self.health = SnapHealth(snapctl=snapctl)
        self.services = SnapServices(snapctl=snapctl)
        self.metadata_files = SnapMetadataFiles(environ=self.environ)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"({self.name} {self.version} {self.revision})"
        )
