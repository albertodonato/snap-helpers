from pathlib import Path

from .._path import SnapPaths


class TestSnapPaths:

    def test_default_env(self, snap_apply_env):
        paths = SnapPaths()
        assert paths.common == Path('/var/snap/mysnap/common')
        assert paths.data == Path('/var/snap/mysnap/123')
        assert paths.snap == Path('/snap/mysnap/123')
        assert paths.user_common == Path('/home/user/snap/mysnap/common')
        assert paths.user_data == Path('/home/s/snap/mysnap/123')

    def test_paths(self, snap_environ):
        paths = SnapPaths(env=snap_environ)
        assert paths.common == Path('/var/snap/mysnap/common')
        assert paths.data == Path('/var/snap/mysnap/123')
        assert paths.snap == Path('/snap/mysnap/123')
        assert paths.user_common == Path('/home/user/snap/mysnap/common')
        assert paths.user_data == Path('/home/s/snap/mysnap/123')

    def test_repr(self, snap_environ):
        paths = SnapPaths(env=snap_environ)
        assert repr(paths) == (
            'SnapPaths('
            'common=/var/snap/mysnap/common '
            'data=/var/snap/mysnap/123 '
            'snap=/snap/mysnap/123 '
            'user_common=/home/user/snap/mysnap/common '
            'user_data=/home/s/snap/mysnap/123)')
