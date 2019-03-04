from copy import deepcopy
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from ._ctl import SnapCtl


class UnknownConfig(Exception):
    """The specified config key is unknown."""

    def __init__(self, key):
        super().__init__(f'Unknown config key: {key}')


class SnapConfig:
    """Interact with the snap configuration.

    This allows fetching the current snap configuration and accessing it as a
    dict.

    Nested keys can be accessed using dotted notation::

      config['foo.bar.baz']

    :param top_level_keys: the top-level configuration keys to load.

    """

    _config: Optional[Dict[str, Any]] = None

    def __init__(
            self, top_level_keys: List[str],
            snapctl: Optional[SnapCtl] = None):
        self._snapctl = snapctl or SnapCtl()
        self._top_level_keys = top_level_keys

    def __getitem__(self, item: str) -> Any:
        """Return value for a configuration key."""
        config = self._config
        for key in item.split('.'):
            if not isinstance(config, dict):
                raise UnknownConfig(item)
            try:
                config = config[key]
            except KeyError:
                raise UnknownConfig(item)
        return config

    def load(self):
        """Load current configuration."""
        self._config = self._snapctl.get(*self._top_level_keys)

    def as_dict(self) -> Dict[str, Any]:
        """Return the current configuration as a :class:`dict`."""
        if self._config is None:
            return {}
        return deepcopy(self._config)
