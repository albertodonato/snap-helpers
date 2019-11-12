from pathlib import Path

import yaml

import pytest

from .._meta import (
    SnapMetadataFile,
    SnapMetadataFiles,
)


@pytest.fixture
def sample_content():
    yield {"foo": {"bar": 3}, "baz": "bza"}


@pytest.fixture
def sample_yaml_file(tmpdir, sample_content):
    path = Path(tmpdir / "sample.yaml")
    with path.open("w") as fd:
        yaml.dump(sample_content, stream=fd)
    yield path


@pytest.fixture
def meta_dir(tmpdir):
    path = Path(tmpdir / "meta")
    path.mkdir()
    yield path


@pytest.fixture
def snap_dir(tmpdir):
    path = Path(tmpdir / "snap")
    path.mkdir()
    yield path


@pytest.fixture
def manifest_yaml(snap_dir):
    content = {"manifest": "content"}
    path = snap_dir / "manifest.yaml"
    with path.open("w") as fd:
        yaml.dump(content, stream=fd)

    yield content


@pytest.fixture
def snapcraft_yaml(snap_dir):
    content = {"snapcraft": "config"}
    path = snap_dir / "snapcraft.yaml"
    with path.open("w") as fd:
        yaml.dump(content, stream=fd)

    yield content


@pytest.fixture
def snap_yaml(meta_dir):
    content = {"snap": "metadata"}
    path = meta_dir / "snap.yaml"
    with path.open("w") as fd:
        yaml.dump(content, stream=fd)

    yield content


@pytest.fixture
def override_snap_dir(monkeypatch, tmpdir):
    monkeypatch.setenv("SNAP", str(tmpdir))


class TestSnapMetadataFile:
    def test_str(self):
        sample = SnapMetadataFile(Path("/some/path"))
        assert str(sample) == "/some/path"

    def test_repr(self):
        sample = SnapMetadataFile(Path("/some/path"))
        assert repr(sample) == "SnapMetadataFile(/some/path)"

    def test_len(self, sample_content, sample_yaml_file):
        metadata_file = SnapMetadataFile(sample_yaml_file)
        assert len(metadata_file) == len(sample_content)

    def test_iter(self, sample_content, sample_yaml_file):
        metadata_file = SnapMetadataFile(sample_yaml_file)
        assert dict(metadata_file) == sample_content

    def test_getitem(self, sample_content, sample_yaml_file):
        metadata_file = SnapMetadataFile(sample_yaml_file)
        assert metadata_file["foo"]["bar"] == sample_content["foo"]["bar"]
        assert metadata_file["baz"] == sample_content["baz"]

    def test_exists_false(self):
        sample = SnapMetadataFile(Path("/not/here"))
        assert not sample.exists()

    def test_exists_true(self, tmpdir):
        path = Path(tmpdir / "sample.yaml")
        path.touch()
        sample = SnapMetadataFile(path)
        assert sample.exists()

    def test_not_found_error(self, tmpdir):
        sample = SnapMetadataFile(Path("/not/here"))
        with pytest.raises(FileNotFoundError):
            dict(sample)


@pytest.mark.usefixtures("override_snap_dir")
class TestSnapMetadataFiles:
    def test_metadata_contents(
        self, monkeypatch, manifest_yaml, snap_yaml, snapcraft_yaml
    ):
        files = SnapMetadataFiles()
        assert dict(files.manifest) == manifest_yaml
        assert dict(files.snap) == snap_yaml
        assert dict(files.snapcraft) == snapcraft_yaml
