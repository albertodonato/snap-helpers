from pathlib import Path
from typing import Optional

from ._env import SnapEnviron


class SnapPaths:
    """Paths related to the snap."""

    __slots__ = ("common", "data", "snap", "user_common", "user_data")

    common: Path  #: the SNAP_COMMON path
    data: Path  #: the SNAP_DATA path
    snap: Path  #: the SNAP path
    user_common: Path  #: the SNAP_USER_COMMON path
    user_data: Path  #: the SNAP_USER_DATA path

    def __init__(self, environ: Optional[SnapEnviron] = None):
        if environ is None:
            environ = SnapEnviron()
        for key in self.__slots__:
            setattr(self, key, Path(environ[key.upper()]))

    def __repr__(self):
        name = self.__class__.__name__
        values = " ".join(f"{key}={str(getattr(self, key))}" for key in self.__slots__)
        return f"{name}({values})"
