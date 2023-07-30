import pytest

from snaphelpers import (
    Snap,
    UnknownConfigKey,
)


@pytest.mark.requires_root
def test_config_set_unset(snap: Snap) -> None:
    # Unset the test keys before running the test proper in case it has been
    # set by another test
    snap.config.unset(["foo", "goo", "test"])
    with pytest.raises(UnknownConfigKey):
        snap.config.get("foo")
    with pytest.raises(UnknownConfigKey):
        snap.config.get("goo")
    snap.config.set({"foo": "bar", "goo": "car"})
    assert snap.config.get("foo") == "bar"
    assert snap.config.get("goo") == "car"
    snap.config.unset(["foo", "goo"])
    with pytest.raises(UnknownConfigKey):
        snap.config.get("foo")
    with pytest.raises(UnknownConfigKey):
        snap.config.get("goo")
    # Check dotted notation correctly creates a dict
    snap.config.set({"test.dotted": "myvalue"})
    assert snap.config.get("test") == {"dotted": "myvalue"}
    # Check removing a key within the dict still leaves the parent key
    snap.config.unset(["test.dotted"])
    assert snap.config.get("test") == {}
    snap.config.set({"test.dotted": "myvalue"})
    # Check removing the top level key removes the whole entry
    snap.config.unset(["test"])
    with pytest.raises(UnknownConfigKey):
        snap.config.get("test")
