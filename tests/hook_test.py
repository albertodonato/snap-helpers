from pkg_resources import (
    Distribution,
    EntryPoint,
)
import pytest

from snaphelpers._hook import (
    get_hooks,
    Hook,
)


class TestHook:
    def test_from_entry_point(self):
        entry_point = EntryPoint.parse(
            "configure = foo.bar:hooks.configure",
            dist=Distribution(project_name="proj"),
        )
        hook = Hook.from_entry_point(entry_point)
        assert hook.name == "configure"
        assert hook.project == "proj"
        assert hook.module == "foo.bar"
        assert hook.import_name == "hooks"
        assert hook.path == "hooks.configure"

    @pytest.mark.parametrize(
        "side_effect,exists",
        [
            (0, True),
            (ImportError("module not found"), False),
        ],
    )
    def test_exists(self, mocker, side_effect, exists):
        entry_point = EntryPoint.parse(
            "configure = foo.bar:hooks.configure",
            dist=Distribution(project_name="proj"),
        )
        mocker.patch.object(entry_point, "resolve").side_effect = [side_effect]
        hook = Hook.from_entry_point(entry_point)
        assert hook.exists == exists

    def test_location(self):
        entry_point = EntryPoint.parse(
            "configure = foo.bar:hooks.configure",
            dist=Distribution(project_name="proj"),
        )
        hook = Hook.from_entry_point(entry_point)
        assert hook.location == "foo.bar:hooks.configure"

    def test_str(self):
        entry_point = EntryPoint.parse(
            "configure = foo.bar:hooks.configure",
            dist=Distribution(project_name="proj"),
        )
        hook = Hook.from_entry_point(entry_point)
        assert str(hook) == "foo.bar:hooks.configure (proj)"


class TestGetHooks:
    def test_hooks(self, mocker, make_entry_points):
        mock_pkg_resources = mocker.Mock()
        mock_pkg_resources.iter_entry_points.return_value = make_entry_points(
            [
                ("pkg1", "configure = pkg1.hooks:hook.configure", True),
                ("pkg2", "install = pkg2.hooks:hook.install", False),
            ]
        )
        hook1, hook2 = get_hooks(pkg_resources=mock_pkg_resources)
        assert hook1.name == "configure"
        assert hook1.exists
        assert hook2.name == "install"
        assert not hook2.exists
