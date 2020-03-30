from copy import deepcopy
from typing import (
    Any,
    Dict,
    Optional,
    Sequence,
)

from ._ctl import SnapCtl


class UnknownConfigKey(Exception):
    """The specified config key is unknown."""

    key: str

    def __init__(self, key: str):
        self.key = key
        super().__init__(f"Unknown config key: {key}")


class InvalidKey(Exception):
    """The specified key is invalid."""

    key: str

    def __init__(self, key: str):
        self.key = key
        super().__init__(f"Invalid top-level key: {key}")


class SnapConfigOptions:
    """Allow accessing a set of Snap config options with a dict-like interface.

    Nested keys can be accessed using dotted notation::

        config['foo.bar.baz']

    :param keys: the top-level configuration keys.

    """

    _config: Optional[Dict[str, Any]] = None

    def __init__(self, keys: Sequence[str], snapctl: Optional[SnapCtl] = None):
        self._keys = list(keys)
        self._snapctl = snapctl or SnapCtl()

    def __getitem__(self, item: str) -> Any:
        """Return value for a configuration key."""
        config = self._config
        for key in item.split("."):
            if not isinstance(config, dict):
                raise UnknownConfigKey(item)
            try:
                config = config[key]
            except KeyError:
                raise UnknownConfigKey(item)
        return config

    def __contains__(self, item: str) -> bool:
        """Whether the configuration conains a key."""
        try:
            self[item]
        except UnknownConfigKey:
            return False
        return True

    def get(self, key: str, default: Any = None) -> Any:
        """Return value for a key, with a default.

        :param key: name of the key to return.
        :param default: value to return if the key is not found.

        """
        try:
            return self[key]
        except UnknownConfigKey:
            return default

    def fetch(self):
        """Fetch (or refresh) configuration for the set of keys."""
        self._config = self._snapctl.config_get(*self._keys)

    def as_dict(self) -> Dict[str, Any]:
        """Return the configuration as a :class:`dict`."""
        if self._config is None:
            return {}
        return deepcopy(self._config)


class SnapConfig:
    """Interact with the snap configuration.

    It allows getting and setting configuration options.

    """

    def __init__(self, snapctl: Optional[SnapCtl] = None):
        self._snapctl = snapctl or SnapCtl()

    def get_options(self, *keys: str) -> SnapConfigOptions:
        """Return a :data:`SnapConfigOptions` for the specified keys.

        :param keys: keys to read configuration for.
        """
        for key in keys:
            if "." in key:
                raise InvalidKey(key)
        options = SnapConfigOptions(keys=keys, snapctl=self._snapctl)
        options.fetch()
        return options

    def get(self, key: str) -> Any:
        """Return value for a single key.

        :param key: key to get config for, possibly with dotted notation.
        :raises UnknownConfigKey: if the option doesn't exist.

        """
        top_key = key.split(".", maxsplit=1)[0]
        options = self.get_options(top_key)
        return options[key]

    def set(self, options: Dict[str, Any]):
        """Set config options.

        :param options: a dict with configs. Keys can use dotted notation.

        """
        self._snapctl.config_set(options)
