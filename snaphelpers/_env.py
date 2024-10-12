import os
from typing import (
    Iterator,
    Mapping,
    Optional,
)


def is_snap(environ: Optional[Mapping[str, str]] = None) -> bool:
    """Return whether running in a Snap.

    :param environ: optionally, the mapping with environment variables.

    """
    if environ is None:
        environ = os.environ
    return bool(environ.get("SNAP", ""))


class NotASnapError(Exception):
    """Not running within a snap environment."""

    def __init__(self) -> None:
        super().__init__(
            "Provided environment is not a snap environment. "
            "Check if the environment is a snap using snaphelpers.is_snap"
        )


class SnapEnviron(Mapping[str, str]):
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
        if not is_snap(environ=environ):
            raise NotASnapError()
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

    def __iter__(self) -> Iterator[str]:
        return iter(self._env)

    def __getattr__(self, attr: str) -> str:
        try:
            return self._env[attr]
        except KeyError as e:
            raise AttributeError(str(e))
