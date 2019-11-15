from pathlib import Path

import yaml

import pytest

from ..snaphelpers import SnapHelpersScript


@pytest.fixture
def src_dir(tmpdir):
    src_dir = Path(tmpdir / "src")
    src_dir.mkdir()
    yield src_dir


@pytest.fixture
def prime_dir(tmpdir):
    prime_dir = Path(tmpdir / "prime")
    prime_dir.mkdir()
    yield prime_dir


@pytest.fixture
def snapcraft_env(monkeypatch, src_dir, prime_dir):
    monkeypatch.setenv("SNAPCRAFT_PART_SRC", str(src_dir))
    monkeypatch.setenv("SNAPCRAFT_PRIME", str(prime_dir))


@pytest.fixture
def snapcraft_yaml(src_dir):
    content = {"hooks": {"install": {}, "configure": {}, "remove": {}}}
    snap_dir = src_dir / "snap"
    snap_dir.mkdir(parents=True)
    snapcraft_yaml = snap_dir / "snapcraft.yaml"
    with snapcraft_yaml.open("w") as fd:
        yaml.dump(content, stream=fd)
    yield snapcraft_yaml


@pytest.mark.usefixtures("snapcraft_env")
class TestSnapHelpersScript:
    def test_write_hooks_missing_part_dir(self, monkeypatch):
        monkeypatch.delenv("SNAPCRAFT_PART_SRC")
        script = SnapHelpersScript()
        with pytest.raises(RuntimeError) as e:
            script(["write-hooks"])
        assert "SNAPCRAFT_PART_SRC environment variable not defined" in str(e.value)

    def test_write_hooks_missing_prime_dir(self, monkeypatch):
        monkeypatch.delenv("SNAPCRAFT_PRIME")
        script = SnapHelpersScript()
        with pytest.raises(RuntimeError) as e:
            script(["write-hooks"])
        assert "SNAPCRAFT_PRIME environment variable not defined" in str(e.value)

    def test_write_hooks_create_files(self, capsys, prime_dir, snapcraft_yaml):
        script = SnapHelpersScript()
        script(["write-hooks"])
        hooks_dir = prime_dir / "snap" / "hooks"
        configure_hook, install_hook, remove_hook = sorted(hooks_dir.iterdir())
        assert (
            '"${SNAP}/bin/snap-helpers-hook" "configure"' in configure_hook.read_text()
        )
        assert '"${SNAP}/bin/snap-helpers-hook" "install"' in install_hook.read_text()
        assert '"${SNAP}/bin/snap-helpers-hook" "remove"' in remove_hook.read_text()
        out = capsys.readouterr().out
        assert "Writing hook files" in out
        assert f"configure -> {hooks_dir}/configure" in out
        assert f"install -> {hooks_dir}/install" in out
        assert f"remove -> {hooks_dir}/remove" in out

    def test_write_hooks_no_hooks(self, capsys, prime_dir, snapcraft_yaml):
        snapcraft_yaml.write_text("{}")
        script = SnapHelpersScript()
        script(["write-hooks"])
        hooks_dir = prime_dir / "snap" / "hooks"
        assert not hooks_dir.exists()
        assert "No hooks defined in the snap" in capsys.readouterr().out

    def test_write_hooks_exlcude(self, capsys, prime_dir, snapcraft_yaml):
        script = SnapHelpersScript()
        script(["write-hooks", "--exclude", "install", "remove"])
        hooks_dir = prime_dir / "snap" / "hooks"
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

    def test_write_hooks_exclude_unknown(self, prime_dir, snapcraft_yaml):
        script = SnapHelpersScript()
        with pytest.raises(RuntimeError) as e:
            script(["write-hooks", "--exclude", "invalid1", "invalid2"])
        assert (
            str(e.value) == "The following hook(s) are not defined: invalid1, invalid2"
        )
