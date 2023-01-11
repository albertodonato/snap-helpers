import pytest

from snaphelpers import Snap

HOOKS = {"configure", "install"}
SERVICES = {"service1", "service2"}


@pytest.fixture
def snap():
    yield Snap()


def test_snap(snap: Snap):
    assert snap.name == "snap-helpers-testapp"
    assert snap.version == "1.0"


@pytest.mark.parametrize("hook", HOOKS)
def test_hook(snap: Snap, hook: str):
    assert (snap.paths.snap / "meta" / "hooks" / hook).exists()


@pytest.mark.parametrize("hook", HOOKS)
def test_hook_called(snap: Snap, hook: str):
    content = (snap.paths.common / "hooks.log").read_text()
    assert f"hooks.{hook} INFO | hook called" in content


@pytest.mark.parametrize("service", SERVICES)
def test_service(snap: Snap, service: str):
    services = snap.services.list()
    assert service in services
    assert services[service].enabled
    assert services[service].active
