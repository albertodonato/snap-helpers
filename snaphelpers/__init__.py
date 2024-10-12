"""Helpers for interacting with the Snap system within a Snap."""

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
    NotASnapError,
    SnapEnviron,
)
from ._health import SnapHealth
from ._path import SnapPaths
from ._service import SnapServices
from ._snap import Snap

__all__ = [
    "InvalidKey",
    "NotASnapError",
    "Snap",
    "SnapConfig",
    "SnapConfigOptions",
    "SnapCtl",
    "SnapCtlError",
    "SnapEnviron",
    "SnapHealth",
    "SnapPaths",
    "SnapServices",
    "UnknownConfigKey",
    "__version__",
    "is_snap",
]

__version__ = "0.4.2"
