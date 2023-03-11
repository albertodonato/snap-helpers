from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterator,
    Mapping,
    Optional,
)

import yaml

from ._env import SnapEnviron


class SnapMetadataFile(Mapping[str, Any]):
    """A YAML metadata file from the snap.

    The content is read at the first access, and is accessible as a regular
    dict.

    """

    path: Path  #: the file Path

    def __init__(self, path: Path):
        self.path = path
        self._loaded = False
        self._data: Dict[str, Any] = {}

    def __str__(self) -> str:
        return str(self.path)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path})"

    def __getitem__(self, item: str) -> Any:
        self._ensure_loaded()
        return self._data[item]

    def __len__(self) -> int:
        self._ensure_loaded()
        return len(self._data)

    def __iter__(self) -> Iterator[str]:
        self._ensure_loaded()
        return iter(self._data)

    def exists(self) -> bool:
        """Return whether the file exists."""
        return self.path.exists()

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return

        with self.path.open() as fd:
            self._data = yaml.safe_load(fd)

        self._loaded = True


class MetadataFileProperty:
    """Wrapper to get :class:`SnapMetadataFile` instances for files."""

    def __init__(self, local_path: str):
        self.local_path = local_path

    def __get__(
        self, instance: "SnapMetadataFiles", owner: type
    ) -> SnapMetadataFile:
        path = Path(instance._environ["SNAP"]) / self.local_path
        return SnapMetadataFile(path)


class SnapMetadataFiles:
    """Metadata files for a snap.

    This provide access to metadata files content via :class:`SnapMetadataFile`
    instances.

    """

    #: Content of the ``snap/metadata.yaml`` file.
    manifest = MetadataFileProperty("snap/manifest.yaml")
    #: Content of the ``meta/snap.yaml`` file.
    snap = MetadataFileProperty("meta/snap.yaml")
    #: Content of the ``snap/snapcraft.yaml`` file.
    snapcraft = MetadataFileProperty("snap/snapcraft.yaml")

    def __init__(self, environ: Optional[SnapEnviron] = None):
        self._environ = environ or SnapEnviron()
