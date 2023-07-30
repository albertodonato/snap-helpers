import os
from typing import Iterator

import pytest

from snaphelpers import Snap


@pytest.fixture
def snap() -> Iterator[Snap]:
    """The snap tests are being run in."""
    yield Snap()


@pytest.fixture(autouse=True)
def requires_root(request: pytest.FixtureRequest) -> None:
    """Skip tests that require to be run as root."""
    marker = request.node.get_closest_marker("requires_root")
    if not marker:
        return
    if os.getuid() != 0:
        pytest.skip("Requires root user")
