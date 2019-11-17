from pathlib import Path

import pytest

from .. import snaphelpers
from ..snaphelpers import (
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
def snapcraft_env(monkeypatch, prime_dir):
    monkeypatch.setenv("SNAPCRAFT_PRIME", str(prime_dir))


@pytest.fixture
def mock_get_hooks(mocker, entry_point_names):
    get_hooks = mocker.patch.object(snaphelpers, "get_hooks")
    get_hooks.side_effect = lambda: {
        name: mocker.Mock(name=f"hook-{name}") for name in entry_point_names
    }
    yield get_hooks


class TestHookScript:
    def test_render(self, hooks_dir):
        script = HookScript("install", hooks_dir)
        assert '"${SNAP}/bin/snap-helpers-hook" "install"' in script.render()

    def test_write(self, hooks_dir):
        hooks_dir.mkdir(parents=True)
        script = HookScript("install", hooks_dir)
        script.write()
        assert '"${SNAP}/bin/snap-helpers-hook" "install"' in script.path().read_text()
        assert script.path().lstat().st_mode & 0o755 == 0o755


@pytest.mark.usefixtures("snapcraft_env", "mock_get_hooks", "prime_dir")
class TestSnapHelpersScript:
    def test_write_hooks_missing_prime_dir(self, monkeypatch):
        monkeypatch.delenv("SNAPCRAFT_PRIME")
        script = SnapHelpersScript()
        with pytest.raises(RuntimeError) as e:
            script(["write-hooks"])
        assert "SNAPCRAFT_PRIME environment variable not defined" in str(e.value)

    def test_write_hooks_create_files(self, capsys, hooks_dir):
        script = SnapHelpersScript()
        script(["write-hooks"])
        configure_hook, install_hook = sorted(hooks_dir.iterdir())
        assert (
            '"${SNAP}/bin/snap-helpers-hook" "configure"' in configure_hook.read_text()
        )
        assert '"${SNAP}/bin/snap-helpers-hook" "install"' in install_hook.read_text()
        out = capsys.readouterr().out
        assert "Writing hook files" in out
        assert f"configure -> {hooks_dir}/configure" in out
        assert f"install -> {hooks_dir}/install" in out

    def test_write_hooks_no_hooks(self, capsys, entry_point_names, hooks_dir):
        entry_point_names.clear()
        script = SnapHelpersScript()
        script(["write-hooks"])
        assert not hooks_dir.exists()
        assert "No hooks defined in the snap" in capsys.readouterr().out

    def test_write_hooks_exlcude(self, capsys, entry_point_names, hooks_dir):
        entry_point_names.append("remove")
        script = SnapHelpersScript()
        script(["write-hooks", "--exclude", "install", "remove"])
        # only the configure hook is created
        [configure_hook] = hooks_dir.iterdir()
        assert (
            '"${SNAP}/bin/snap-helpers-hook" "configure"' in configure_hook.read_text()
        )
        out = capsys.readouterr().out
        assert "Writing hook files" in out
        assert f"configure -> {hooks_dir}/configure" in out
        assert f"install -> {hooks_dir}/install" not in out
        assert f"remove -> {hooks_dir}/remove" not in out

    def test_write_hooks_exclude_unknown(self):
        script = SnapHelpersScript()
        with pytest.raises(RuntimeError) as e:
            script(["write-hooks", "--exclude", "invalid1", "invalid2"])
        assert (
            str(e.value) == "The following hook(s) are not defined: invalid1, invalid2"
        )
