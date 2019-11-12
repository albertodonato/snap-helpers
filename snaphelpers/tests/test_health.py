from unittest.mock import call

import pytest

from .._health import SnapHealth


@pytest.fixture
def snaphealth(snapctl):
    yield SnapHealth(snapctl=snapctl)


class TestSnapHealth:
    def test_okay(self, snapctl, snaphealth):
        snaphealth.okay()
        assert snapctl.run.mock_calls == [call("set-health", "okay")]

    @pytest.mark.parametrize("status", ["waiting", "blocked", "error"])
    def test_other_statuses(self, snapctl, snaphealth, status):
        method = getattr(snaphealth, status)
        method("some message")
        assert snapctl.run.mock_calls == [call("set-health", status, "some message")]

    @pytest.mark.parametrize("status", ["waiting", "blocked", "error"])
    def test_other_statuses_code(self, snapctl, snaphealth, status):
        method = getattr(snaphealth, status)
        method("some message", code="a-b-c")
        assert snapctl.run.mock_calls == [
            call("set-health", status, "some message", "--code", "a-b-c")
        ]

    @pytest.mark.parametrize("status", ["waiting", "blocked", "error"])
    def test_other_statuses_missing_message(self, snapctl, snaphealth, status):
        method = getattr(snaphealth, status)
        with pytest.raises(ValueError) as err:
            method("")
        assert str(err.value) == "Health status message must not be empty"

    @pytest.mark.parametrize("status", ["waiting", "blocked", "error"])
    def test_other_statuses_invalid_code(self, snapctl, snaphealth, status):
        method = getattr(snaphealth, status)
        with pytest.raises(ValueError) as err:
            method("some message", code="foo bar")
        assert str(err.value) == "Invalid health status code format"
