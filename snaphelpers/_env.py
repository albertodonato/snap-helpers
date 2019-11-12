from collections import abc
import os
from typing import (
    Iterator,
    Mapping,
    Optional,
)


def is_snap(environ: Optional[Mapping[str, str]] = None) -> bool:
    """Return whether running in a Snap."""
    if environ is None:
        environ = os.environ
    return bool(environ.get("SNAP", ""))


class SnapEnviron(abc.Mapping):
    """Environment variables related to the Snap.

    This provides read-only access to environment variables starting with
    :data:`SNAP_`.

    These can be accessed either as a dict or as attributes, without the
    :data:`SNAP_` prefix. E.g.::

      env = SnapEnviron()
      env.NAME     # -> 'mysnap'
      env['NAME']  # -> 'mysnap'

    *Note*: The :data:`SNAP` environment variable is also included.

    """

    _PREFIX = "SNAP_"

    def __init__(self, environ: Optional[Mapping[str, str]] = None):
        if environ is None:
            environ = os.environ
        prefix_len = len(self._PREFIX)
        self._env = {
            key[prefix_len:]: value
            for key, value in environ.items()
            if key.startswith(self._PREFIX)
        }
        self._env["SNAP"] = environ["SNAP"]

    def __getitem__(self, key: str) -> str:
        return self._env[key]

    def __len__(self) -> int:
        return len(self._env)

    def __iter__(self) -> Iterator:
        return iter(self._env)

    def __getattr__(self, attr: str) -> str:
        try:
            return self._env[attr]
        except KeyError as e:
            raise AttributeError(str(e))
