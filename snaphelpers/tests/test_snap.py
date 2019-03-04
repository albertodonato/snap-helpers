import pytest

from .._snap import Snap


class TestSnap:

    @pytest.mark.parametrize(
        'name', ['name', 'instance_name', 'version', 'revision'])
    def test_properties(self, name, snap_environ):
        snap = Snap(environ=snap_environ)
        assert getattr(snap, name) == snap_environ[f'SNAP_{name.upper()}']
