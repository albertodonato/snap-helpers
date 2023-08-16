from snaphelpers import Snap


def test_snap(snap: Snap) -> None:
    assert snap.name == "snap-helpers-testapp"
    assert snap.version == "1.0"
