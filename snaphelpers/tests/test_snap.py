from pathlib import Path

import pytest

from .._snap import Snap


class TestSnap:
    def test_str(self, snap_env):
        snap = Snap(environ=snap_env)
        assert str(snap) == "Snap(mysnap 0.1.2 123)"

    @pytest.mark.parametrize("name", ["name", "instance_name", "version", "revision"])
    def test_properties(self, name, snap_env):
        snap = Snap(environ=snap_env)
        assert getattr(snap, name) == snap_env[f"SNAP_{name.upper()}"]

    def test_paths(self, snap_env):
        snap = Snap(environ=snap_env)
        assert snap.paths.snap == Path("/snap/mysnap/123")
        assert snap.paths.common == Path("/var/snap/mysnap/common")
