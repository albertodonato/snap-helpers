# Copyright Alberto Donato 2019, 2026
# SPDX-License-Identifier: LGPL-3.0-or-later

from snaphelpers import Snap


def test_snap(snap: Snap) -> None:
    assert snap.name == "snap-helpers-testapp"
    assert snap.version == "1.0"
