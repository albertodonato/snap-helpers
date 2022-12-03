from pathlib import Path
from typing import Optional

from ._env import SnapEnviron


class SnapPaths:
    """Paths related to the snap."""

    __slots__ = ("common", "data", "real_home", "snap", "user_common", "user_data")

    common: Path  #: the SNAP_COMMON path
    data: Path  #: the SNAP_DATA path
    real_home: Path  #: the SNAP_REAL_HOME path
    snap: Path  #: the SNAP path
    user_common: Path  #: the SNAP_USER_COMMON path
    user_data: Path  #: the SNAP_USER_DATA path

    def __init__(self, env: Optional[SnapEnviron] = None):
        if env is None:
            env = SnapEnviron()
        for key in self.__slots__:
            setattr(self, key, Path(env[key.upper()]))

    def __repr__(self):
        name = self.__class__.__name__
        values = " ".join(f"{key}={str(getattr(self, key))}" for key in self.__slots__)
        return f"{name}({values})"
