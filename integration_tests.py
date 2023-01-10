import pytest

from snaphelpers import Snap
from snaphelpers._conf import UnknownConfigKey

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


def test_config_set_unset(snap: Snap):
    # Unset the test keys before running the test proper just in case
    # it has been set by another test.
    snap.config.unset(["foo", "goo", "test"])
    with pytest.raises(UnknownConfigKey):
        assert snap.config.get("foo")
    with pytest.raises(UnknownConfigKey):
        assert snap.config.get("goo")
    snap.config.set({"foo": "bar", "goo": "car"})
    assert snap.config.get("foo") == "bar"
    assert snap.config.get("goo") == "car"
    snap.config.unset(["foo", "goo"])
    with pytest.raises(UnknownConfigKey):
        assert snap.config.get("foo")
    with pytest.raises(UnknownConfigKey):
        assert snap.config.get("goo")
    # Check dotted notation correctly creates a dict
    snap.config.set({"test.dotted": "myvalue"})
    assert snap.config.get("test") == {"dotted": "myvalue"}
    # Check removing a key within the dict still leaves the
    # parent key
    snap.config.unset(["test.dotted"])
    assert snap.config.get("test") == {}
    snap.config.set({"test.dotted": "myvalue"})
    # Check removing the top level key removes the whole
    # entry.
    snap.config.unset(["test"])
    with pytest.raises(UnknownConfigKey):
        snap.config.get("test")
