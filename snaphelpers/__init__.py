"""Helpers for interacting with the Snap system within a Snap."""

from packaging.version import parse
from pkg_resources import get_distribution

from ._conf import (
    InvalidKey,
    SnapConfig,
    SnapConfigOptions,
    UnknownConfigKey,
)
from ._ctl import (
    SnapCtl,
    SnapCtlError,
)
from ._env import (
    is_snap,
    SnapEnviron,
)
from ._health import SnapHealth
from ._path import SnapPaths
from ._service import SnapServices
from ._snap import Snap

__all__ = [
    "is_snap",
    "InvalidKey",
    "Snap",
    "SnapCtl",
    "SnapCtlError",
    "SnapConfig",
    "SnapConfigOptions",
    "SnapEnviron",
    "SnapHealth",
    "SnapPaths",
    "SnapServices",
    "UnknownConfigKey",
    "__version__",
]

__version__ = parse(get_distribution("snap-helpers").version)
