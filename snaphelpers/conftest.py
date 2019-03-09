from copy import deepcopy

import pytest

from ._env import SnapEnviron


@pytest.fixture
def snap_env():
    """Environment variables defined in a snap."""
    yield {
        'SNAP': '/snap/mysnap/123',
        'SNAP_COMMON': '/var/snap/mysnap/common',
        'SNAP_DATA': '/var/snap/mysnap/123',
        'SNAP_INSTANCE_NAME': 'mysnap_inst',
        'SNAP_NAME': 'mysnap',
        'SNAP_REVISION': '123',
        'SNAP_USER_COMMON': '/home/user/snap/mysnap/common',
        'SNAP_USER_DATA': '/home/s/snap/mysnap/123',
        'SNAP_VERSION': '0.1.2'
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
        'foo': 123,
        'bar': 'BAR',
        'baz': {
            'aaa': 'nested',
            'bbb': {
                'ccc': 'more nested'
            }
        },
        'blah': [1, 2, 3]
    }


class FakeSnapCtl:

    def __init__(self, configs):
        self.configs = configs

    def get(self, *keys):
        options = {}
        for key in keys:
            if key in self.configs:
                options[key] = deepcopy(self.configs[key])
        return options

    def set(self, configs):
        for key, value in configs.items():
            old_conf = conf = self.configs
            for token in key.split('.'):
                entry = conf.get(token)
                if not isinstance(entry, dict):
                    conf[token] = {}

                old_conf, conf = conf, conf[token]
            old_conf[token] = value


@pytest.fixture
def snapctl(snap_config):
    """A fake SnapCtl handling the config."""
    yield FakeSnapCtl(configs=snap_config)
