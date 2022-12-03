from copy import deepcopy

from pkg_resources import (
    Distribution,
    EntryPoint,
)
import pytest

from ._ctl import SnapCtl
from ._env import SnapEnviron


@pytest.fixture
def snap_env():
    """Environment variables defined in a snap."""
    yield {
        "SNAP": "/snap/mysnap/123",
        "SNAP_COMMON": "/var/snap/mysnap/common",
        "SNAP_DATA": "/var/snap/mysnap/123",
        "SNAP_INSTANCE_NAME": "mysnap_inst",
        "SNAP_NAME": "mysnap",
        "SNAP_REAL_HOME": "/home/user",
        "SNAP_REVISION": "123",
        "SNAP_USER_COMMON": "/home/user/snap/mysnap/common",
        "SNAP_USER_DATA": "/home/user/snap/mysnap/123",
        "SNAP_VERSION": "0.1.2",
    }


@pytest.fixture
def snap_environ(snap_env):
    """A SnapEnviron using the snap_env."""
    yield SnapEnviron(environ=snap_env)


@pytest.fixture
def snap_apply_env(monkeypatch, snap_env):
    """Apply snap environment variables."""
    for key, value in snap_env.items():
        monkeypatch.setenv(key, value)


@pytest.fixture
def snap_config():
    """A sample snap configuration."""
    yield {
        "foo": 123,
        "bar": "BAR",
        "baz": {"aaa": "nested", "bbb": {"ccc": "more nested"}},
        "blah": [1, 2, 3],
    }


@pytest.fixture
def snapctl(mocker, snap_apply_env):
    """A SnapCtl instance with a mocked run method."""
    snapctl = SnapCtl(executable="/not/here")
    snapctl.run = mocker.Mock(return_value="")
    yield snapctl


class FakeSnapCtl:
    """A fake SnapCtl implementation."""

    def __init__(self, configs=None, services=None):
        self._configs = configs or {}
        self._services = services or []

    def config_get(self, *keys):
        options = {}
        for key in keys:
            if key in self._configs:
                options[key] = deepcopy(self._configs[key])
        return options

    def config_set(self, configs):
        for key, value in configs.items():
            old_conf = conf = self._configs
            for token in key.split("."):
                entry = conf.get(token)
                if not isinstance(entry, dict):
                    conf[token] = {}

                old_conf, conf = conf, conf[token]
            old_conf[token] = value

    def services(self):
        return deepcopy(self._services)


@pytest.fixture
def fake_snapctl(snap_config):
    """A fake SnapCtl handling the config."""
    yield FakeSnapCtl(configs=snap_config)


@pytest.fixture
def make_entry_points():
    """Return an iterable with EntryPoint objects."""

    def make(defs):
        entry_points = []
        for project_name, definition, exists in defs:

            if exists:

                def resolve():
                    pass

            else:

                def resolve():
                    raise ImportError(f"Failed importing {definition}")

            entry_point = EntryPoint.parse(
                definition, dist=Distribution(project_name=project_name)
            )
            entry_point.resolve = resolve
            entry_points.append(entry_point)
        return entry_points

    yield make
