import json
from textwrap import dedent

import pytest

from ._ctl import SnapCtl


@pytest.fixture
def snap_environ():
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
def snap_apply_environ(monkeypatch, snap_environ):
    """Apply snap environment variables."""
    for key, value in snap_environ.items():
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


@pytest.fixture
def snapctl(tmpdir, snap_environ, snap_config):
    """A SnapCtl instance returning the config."""
    executable = tmpdir / 'snapctl'
    executable.write_text(
        dedent(
            f'''\
            #!/bin/sh
            cat <<EOF
            {json.dumps(snap_config)}
            EOF
            '''), 'utf-8')
    executable.chmod(0o755)
    yield SnapCtl(executable=str(executable), environ=snap_environ)
