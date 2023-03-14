from io import StringIO
from pathlib import Path
from textwrap import dedent

import pytest

from snaphelpers._hook import Hook
from snaphelpers.scripts import snap_helpers
from snaphelpers.scripts.snap_helpers import (
    HookScript,
    SnapHelpersScript,
)


@pytest.fixture
def prime_dir(tmpdir):
    prime_dir = Path(tmpdir / "prime")
    prime_dir.mkdir()
    yield prime_dir


@pytest.fixture
def hooks_dir(prime_dir):
    yield prime_dir / "snap" / "hooks"


@pytest.fixture
def mock_get_hooks(mocker, make_entry_points):
    defs = [
        ("pkg1", "configure = pkg1.hooks:hook.configure", True),
        ("pkg2", "install = pkg2.hooks:hook.install", True),
    ]

    def mock(defs=defs):
        hooks = [
            Hook.from_entry_point(entry_point)
            for entry_point in make_entry_points(defs)
        ]
        get_hooks = mocker.patch.object(snap_helpers, "get_hooks")
        get_hooks.return_value = hooks
        return get_hooks

    yield mock


@pytest.fixture
def snapcraft_env(monkeypatch, prime_dir):
    monkeypatch.setenv("CRAFT_PRIME", str(prime_dir))


@pytest.fixture
def script():
    yield SnapHelpersScript(stdout=StringIO(), stderr=StringIO())


class TestHookScript:
    def test_render(self):
        hook = Hook(
            name="install",
            project="foo",
            module="foo.bar",
            import_name="hooks",
            path="hooks.install",
            exists=True,
        )
        hookscript = HookScript(hook)
        script = hookscript.render()
        assert "from foo.bar import hooks" in script
        assert "sys.exit(hooks.install(Snap()))" in script

    def test_write(self, hooks_dir):
        hooks_dir.mkdir(parents=True)
        hook = Hook(
            name="install",
            project="foo",
            module="foo.bar",
            import_name="hooks",
            path="hooks.install",
            exists=True,
        )
        hookscript = HookScript(hook)
        hookscript.write(hooks_dir)
        script_path = hooks_dir / "install"
        assert script_path.lstat().st_mode & 0o755 == 0o755
        script = script_path.read_text()
        assert "from foo.bar import hooks" in script
        assert "sys.exit(hooks.install(Snap()))" in script


@pytest.mark.usefixtures("snapcraft_env", "prime_dir")
class TestSnapHelpersScript:
    def test_write_hooks_missing_prime_dir_env_var(
        self, monkeypatch, script, mock_get_hooks
    ):
        mock_get_hooks()
        monkeypatch.delenv("CRAFT_PRIME")
        assert script(["write-hooks"]) == 1
        assert (
            script.stderr.getvalue()
            == "CRAFT_PRIME environment variable not defined\n"
        )

    def test_write_hooks_missing_prime_dir_env_var_fallback(
        self,
        monkeypatch,
        script,
        prime_dir,
        hooks_dir,
        mock_get_hooks,
    ):
        mock_get_hooks()
        monkeypatch.delenv("CRAFT_PRIME")
        monkeypatch.setenv("SNAPCRAFT_PRIME", str(prime_dir))
        assert script(["write-hooks"]) == 0
        configure_hook, install_hook = sorted(hooks_dir.iterdir())
        assert "sys.exit(hook.configure(Snap()))" in configure_hook.read_text()
        assert "sys.exit(hook.install(Snap()))" in install_hook.read_text()
        assert f"Writing hook files to {hooks_dir}" in script.stdout.getvalue()

    def test_write_hooks_specify_dir(
        self,
        script,
        prime_dir,
        hooks_dir,
        mock_get_hooks,
    ):
        mock_get_hooks()
        assert script(["write-hooks", "--prime-dir", str(prime_dir)]) == 0
        configure_hook, install_hook = sorted(hooks_dir.iterdir())
        assert "sys.exit(hook.configure(Snap()))" in configure_hook.read_text()
        assert "sys.exit(hook.install(Snap()))" in install_hook.read_text()
        assert f"Writing hook files to {hooks_dir}" in script.stdout.getvalue()

    def test_write_hooks_create_files(self, script, hooks_dir, mock_get_hooks):
        mock_get_hooks()
        assert script(["write-hooks"]) == 0
        configure_hook, install_hook = sorted(hooks_dir.iterdir())
        assert "sys.exit(hook.configure(Snap()))" in configure_hook.read_text()
        assert "sys.exit(hook.install(Snap()))" in install_hook.read_text()
        assert f"Writing hook files to {hooks_dir}" in script.stdout.getvalue()

    def test_write_hooks_no_hooks(self, script, hooks_dir, mock_get_hooks):
        mock_get_hooks(defs=[])
        assert script(["write-hooks"]) == 0
        assert not hooks_dir.exists()
        assert "No hooks defined in the snap" in script.stdout.getvalue()

    def test_write_hooks_no_hooks_fail_empty(
        self, script, hooks_dir, mock_get_hooks
    ):
        mock_get_hooks(defs=[])
        assert script(["write-hooks", "--fail-empty"]) == 1
        assert not hooks_dir.exists()
        assert "No hooks defined in the snap" in script.stdout.getvalue()

    def test_write_hooks_duplicated_hooks(
        self, script, hooks_dir, mock_get_hooks
    ):
        mock_get_hooks(
            defs=[
                ("pkg1", "configure = pkg1.hooks:hook.configure", True),
                ("pkg2", "configure = pkg2.hooks:hook.configure", True),
                ("pkg3", "install = pkg3.hooks:hook.install", True),
                ("pkg4", "install = pkg4.hooks:hook.install", True),
            ]
        )
        assert script(["write-hooks"]) == 1
        assert not hooks_dir.exists()
        assert script.stderr.getvalue() == dedent(
            """\
            Multiple definitions found for hook(s):
            - configure
                pkg1.hooks:hook.configure (pkg1)
                pkg2.hooks:hook.configure (pkg2)
            - install
                pkg3.hooks:hook.install (pkg3)
                pkg4.hooks:hook.install (pkg4)
            """
        )

    def test_write_hooks_not_found(self, script, hooks_dir, mock_get_hooks):
        mock_get_hooks(
            defs=[
                ("pkg1", "configure = pkg1.hooks:hook.configure", True),
                ("pkg2", "install = pkg2.hooks:hook.install", False),
            ]
        )
        assert script(["write-hooks"]) == 1
        assert not hooks_dir.exists()
        assert script.stderr.getvalue() == dedent(
            """\
            Hook function(s) not found:
            - pkg2.hooks:hook.install (pkg2)
            """
        )
