import json
from textwrap import dedent

import pytest

from .._ctl import (
    ServiceInfo,
    SnapCtl,
)


@pytest.fixture
def snapctl_calls():
    yield []


@pytest.fixture
def snapctl(snap_apply_env, snapctl_calls):
    snapctl = SnapCtl(executable='/not/here')
    snapctl._run = lambda *args: snapctl_calls.append(args)
    snapctl.output = ''

    def run(*args):
        snapctl_calls.append(args)
        return snapctl.output

    snapctl._run = run
    yield snapctl


@pytest.mark.usefixtures('snap_apply_env')
class TestSnapCtl:

    def test_get(self, tmpdir):
        executable = tmpdir / 'snapctl'
        data = {'foo': 123, 'bar': 'baz'}
        executable.write_text(
            dedent(
                f'''\
                #!/bin/sh
                cat <<EOF
                {json.dumps(data)}
                EOF
                '''), 'utf-8')
        executable.chmod(0o755)
        snapctl = SnapCtl(executable=str(executable))
        assert snapctl.get('foo', 'bar') == data

    def test_get_calls(self, snapctl, snapctl_calls):
        snapctl.output = '{}'
        snapctl.get('foo', 'bar')
        assert snapctl_calls == [('get', '-d', 'foo', 'bar')]

    def test_set(self, snapctl, snapctl_calls):
        snapctl.set({'foo.bar': 123, 'baz': [1, 2, 3]})
        assert snapctl_calls == [('set', 'foo.bar=123', 'baz=[1, 2, 3]')]

    def test_start(self, snapctl, snapctl_calls):
        snapctl.start()
        assert snapctl_calls == [('start', )]

    def test_start_enable(self, snapctl, snapctl_calls):
        snapctl.start(enable=True)
        assert snapctl_calls == [('start', '--enable')]

    def test_start_services(self, snapctl, snapctl_calls):
        snapctl.start('foo', 'bar')
        assert snapctl_calls == [
            ('start', 'mysnap_inst.foo', 'mysnap_inst.bar')
        ]

    def test_stop(self, snapctl, snapctl_calls):
        snapctl.stop()
        assert snapctl_calls == [('stop', )]

    def test_stop_enable(self, snapctl, snapctl_calls):
        snapctl.stop(disable=True)
        assert snapctl_calls == [('stop', '--disable')]

    def test_stop_services(self, snapctl, snapctl_calls):
        snapctl.stop('foo', 'bar')
        assert snapctl_calls == [
            ('stop', 'mysnap_inst.foo', 'mysnap_inst.bar')
        ]

    def test_services(self, tmpdir):
        executable = tmpdir / 'snapctl'
        executable.write_text(
            dedent(
                f'''\
                #!/bin/sh
                cat <<EOF
                Service          Startup   Current   Notes
                mysnap.service1  disabled  inactive  foo,bar
                mysnap.service2  enabled   active    -
                mysnap.service3  enabled   inactive  baz
                EOF
                '''), 'utf-8')
        executable.chmod(0o755)
        snapctl = SnapCtl(executable=str(executable))
        assert snapctl.services() == [
            ServiceInfo(
                name='service1',
                enabled=False,
                active=False,
                notes=['foo', 'bar']),
            ServiceInfo(name='service2', enabled=True, active=True, notes=[]),
            ServiceInfo(
                name='service3', enabled=True, active=False, notes=['baz'])
        ]
