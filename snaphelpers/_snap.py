from typing import (
    Mapping,
    Optional,
)

from ._ctl import SnapCtl
from ._env import SnapEnviron


class EnvironProperty:
    """Wrapper to get properties from a :class:`SanpEnviron` instance."""

    def __init__(self, name: str):
        self.name = name

    def __get__(self, instance, owner):
        return getattr(instance.environ, self.name)


class Snap:
    """Top-level wrapper for a Snap."""

    environ: SnapEnviron
    ctl: SnapCtl

    def __init__(self, environ: Optional[Mapping[str, str]] = None):
        self.environ = SnapEnviron(environ=environ)
        self.ctl = SnapCtl(environ=environ)

    name = EnvironProperty('NAME')
    instance_name = EnvironProperty('INSTANCE_NAME')
    version = EnvironProperty('VERSION')
    revision = EnvironProperty('REVISION')
