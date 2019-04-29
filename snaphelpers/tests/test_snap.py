from pathlib import Path

from .._snap import Snap


class TestSnap:

    def test_str(self, snap_env):
        snap = Snap(environ=snap_env)
        assert str(snap) == 'Snap(mysnap 0.1.2 123)'

    def test_properties(self, snap_env):
        snap = Snap(environ=snap_env)
        assert snap.name == 'mysnap'
        assert snap.instance_name == 'mysnap_inst'
        assert snap.version == '0.1.2'
        assert snap.revision == 123

    def test_revision_invalid(self, snap_env):
        snap_env['SNAP_REVISION'] = 'invald'
        snap = Snap(environ=snap_env)
        assert snap.revision is None

    def test_paths(self, snap_env):
        snap = Snap(environ=snap_env)
        assert snap.paths.snap == Path('/snap/mysnap/123')
        assert snap.paths.common == Path('/var/snap/mysnap/common')
