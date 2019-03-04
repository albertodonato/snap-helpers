import pytest

from .._env import (
    is_snap,
    SnapEnviron,
)


class TestIsSnap:

    @pytest.mark.parametrize(
        'value,expected', [('/snap/mysnap/12', True), ('', False)])
    def test_with_env(self, value, expected):
        environ = {'SNAP': value}
        assert is_snap(environ=environ) == expected

    def test_default_env(self, snap_apply_environ):
        assert is_snap()


class TestSnapEnviron:

    def test_to_dict(self, snap_environ):
        # ignored environment variables
        snap_environ.update({'OTHER': 'value', 'PATH': '/bin:/usr/bin'})
        env = SnapEnviron(environ=snap_environ)
        assert dict(env) == {
            'NAME': 'mysnap',
            'COMMON': '/var/snap/mysnap/common',
            'DATA': '/var/snap/mysnap/123',
            'INSTANCE_NAME': 'mysnap_inst',
            'REVISION': '123',
            'SNAP': '/snap/mysnap/123',
            'USER_COMMON': '/home/user/snap/mysnap/common',
            'USER_DATA': '/home/s/snap/mysnap/123',
            'VERSION': '0.1.2'
        }

    def test_len(self, snap_environ):
        env = SnapEnviron(environ=snap_environ)
        assert len(env) == len(snap_environ)

    def test_getitem(self, snap_environ):
        env = SnapEnviron(environ=snap_environ)
        assert env['DATA'] == '/var/snap/mysnap/123'

    def test_setitem_not_allowed(self, snap_environ):
        env = SnapEnviron(environ=snap_environ)
        with pytest.raises(TypeError):
            env['FOO'] = 'bar'

    def test_getattr(self, snap_environ):
        env = SnapEnviron(environ=snap_environ)
        assert env.VERSION == '0.1.2'

    def test_getattr_not_found(self, snap_environ):
        env = SnapEnviron(environ=snap_environ)
        with pytest.raises(AttributeError):
            env.FOO

    def test_default_env(self, snap_environ, snap_apply_environ):
        assert SnapEnviron().SNAP == snap_environ['SNAP']
