from typing import (
    Any,
    Callable,
    Mapping,
    Optional,
)

from ._conf import SnapConfig
from ._ctl import SnapCtl
from ._env import SnapEnviron
from ._path import SnapPaths
from ._service import SnapServices


class EnvironProperty:
    """Wrapper to get properties from a :class:`SanpEnviron` instance."""

    def __init__(self, name: str, converter: Callable[[str], Any] = str):
        self.name = name
        self.converter = converter

    def __get__(self, instance, owner):
        value = getattr(instance.environ, self.name)
        try:
            return self.converter(value)
        except ValueError:
            return None


class Snap:
    """Top-level wrapper for a Snap."""

    config: SnapConfig
    environ: SnapEnviron
    paths: SnapPaths
    services: SnapServices

    def __init__(self, environ: Optional[Mapping[str, str]] = None):
        self.environ = SnapEnviron(environ=environ)
        self.paths = SnapPaths(env=self.environ)
        snapctl = SnapCtl(env=self.environ)
        self.config = SnapConfig(snapctl=snapctl)
        self.services = SnapServices(snapctl=snapctl)

    def __str__(self):
        return (
            f'{self.__class__.__name__}'
            f'({self.name} {self.version} {self.revision})')

    name = EnvironProperty('NAME')
    instance_name = EnvironProperty('INSTANCE_NAME')
    version = EnvironProperty('VERSION')
    revision = EnvironProperty('REVISION', converter=int)
