import pytest

from .._hook import get_hooks


@pytest.fixture
def mock_pkg_resources(mocker, entry_points):
    pkg_resources = mocker.Mock()
    pkg_resources.iter_entry_points.return_value = entry_points
    yield pkg_resources


class TestGetHooks:
    def test_hooks(self, mock_pkg_resources, snap_hooks_calls):
        assert get_hooks(pkg_resources=mock_pkg_resources) == {
            "configure": "loaded-configure",
            "install": "loaded-install",
        }
        assert snap_hooks_calls == ["configure", "install"]
