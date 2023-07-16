import pytest

from snaphelpers._hook import (
    get_hooks,
    Hook,
)
from snaphelpers._importlib import EntryPoint


class TestHook:
    def test_from_entry_point(self, make_entry_points):
        [entry_point] = make_entry_points(
            ("proj", "configure = foo.bar:hooks.configure")
        )
        hook = Hook.from_entry_point(entry_point)
        assert hook.name == "configure"
        assert hook.project == "proj"
        assert hook.module == "foo.bar"
        assert hook.import_name == "hooks"
        assert hook.path == "hooks.configure"

    @pytest.mark.parametrize(
        "definition,exists",
        [
            ("os:getpid", True),
            ("not.here:fail", False),
        ],
    )
    def test_exists(self, definition, exists):
        entry_point = EntryPoint(
            name="configure",
            value=definition,
            group="snaphelpers.hooks",
        )
        hook = Hook.from_entry_point(entry_point)
        assert hook.exists == exists

    def test_location(self, make_entry_points):
        [entry_point] = make_entry_points(
            ("proj", "configure = foo.bar:hooks.configure")
        )
        hook = Hook.from_entry_point(entry_point)
        assert hook.location == "foo.bar:hooks.configure"

    def test_str(self, make_entry_points):
        [entry_point] = make_entry_points(
            ("proj", "configure = foo.bar:hooks.configure")
        )
        hook = Hook.from_entry_point(entry_point)
        assert str(hook) == "foo.bar:hooks.configure (proj)"


class TestGetHooks:
    def test_hooks(self, make_entry_points):
        def entry_points(group=None):
            return make_entry_points(
                ("pkg1", "configure = os:getpid"),
                ("pkg2", "install = not.here:fail"),
            )

        hook1, hook2 = get_hooks(entry_points=entry_points)
        assert hook1.name == "configure"
        assert hook1.exists
        assert hook2.name == "install"
        assert not hook2.exists
