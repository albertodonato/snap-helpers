import pytest

from snaphelpers import Snap

HOOKS = {"configure", "install"}


@pytest.mark.parametrize("hook", HOOKS)
def test_hook(snap: Snap, hook: str) -> None:
    assert (snap.paths.snap / "meta" / "hooks" / hook).exists()


@pytest.mark.parametrize("hook", HOOKS)
def test_hook_called(snap: Snap, hook: str) -> None:
    content = (snap.paths.common / "hooks.log").read_text()
    assert f"hooks.{hook} INFO | hook called" in content
