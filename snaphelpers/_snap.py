from typing import (
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

    def __get__(self, instance, owner):
        return getattr(instance.environ, self.name)


class Snap:
    """Top-level wrapper for a Snap."""

    config: SnapConfig
    environ: SnapEnviron
    health: SnapHealth
    paths: SnapPaths
    services: SnapServices
    metadata_files: SnapMetadataFiles

    name = EnvironProperty("NAME")
    instance_name = EnvironProperty("INSTANCE_NAME")
    version = EnvironProperty("VERSION")
    revision = EnvironProperty("REVISION")

    def __init__(self, environ: Optional[Mapping[str, str]] = None):
        self.environ = SnapEnviron(environ=environ)
        self.paths = SnapPaths(env=self.environ)
        snapctl = SnapCtl(env=self.environ)
        self.config = SnapConfig(snapctl=snapctl)
        self.health = SnapHealth(snapctl=snapctl)
        self.services = SnapServices(snapctl=snapctl)
        self.metadata_files = SnapMetadataFiles(environ=self.environ)

    def __str__(self):
        return (
            f"{self.__class__.__name__}" f"({self.name} {self.version} {self.revision})"
        )
