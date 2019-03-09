from pathlib import Path

import pytest

from .._snap import Snap


class TestSnap:

    def test_str(self, snap_environ):
        snap = Snap(environ=snap_environ)
        assert str(snap) == 'Snap(mysnap 0.1.2 123)'

    @pytest.mark.parametrize(
        'name', ['name', 'instance_name', 'version', 'revision'])
    def test_properties(self, name, snap_environ):
        snap = Snap(environ=snap_environ)
        assert getattr(snap, name) == snap_environ[f'SNAP_{name.upper()}']

    def test_paths(self, snap_environ):
        snap = Snap(environ=snap_environ)
        assert snap.paths.snap == Path('/snap/mysnap/123')
        assert snap.paths.common == Path('/var/snap/mysnap/common')
