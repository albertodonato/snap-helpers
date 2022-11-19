import pytest
from snaphelpers import Snap

HOOKS = {"configure", "install"}


@pytest.fixture
def snap():
    yield Snap()


def test_snap(snap: Snap):
    assert snap.name == "testapp"
    assert snap.version == "1.0"


@pytest.mark.parametrize("hook", HOOKS)
def test_hook(snap: Snap, hook: str):
    assert (snap.paths.snap / "meta" / "hooks" / hook).exists()


@pytest.mark.parametrize("hook", HOOKS)
def test_hook_called(snap: Snap, hook: str):
    content = (snap.paths.common / f"{hook}.log").read_text()
    assert f"{hook} called" in content
