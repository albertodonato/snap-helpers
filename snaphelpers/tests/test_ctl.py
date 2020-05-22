import json
from textwrap import dedent
from unittest.mock import call

import pytest

from .._ctl import (
    ServiceInfo,
    SnapCtl,
    SnapCtlError,
    SnapHealthStatus,
)


@pytest.mark.usefixtures("snap_apply_env")
class TestSnapCtl:
    def test_run(self, tmpdir):
        executable = tmpdir / "snapctl"
        executable.write_text(
            dedent(
                """\
                #!/bin/sh
                echo foo bar
                """
            ),
            "utf-8",
        )
        executable.chmod(0o755)
        snapctl = SnapCtl(executable=str(executable))
        assert snapctl.run() == "foo bar\n"

    def test_run_fail(self, tmpdir):
        executable = tmpdir / "snapctl"
        executable.write_text(
            dedent(
                """\
                #!/bin/sh
                echo 'fail!' >&2
                exit 1
                """
            ),
            "utf-8",
        )
        executable.chmod(0o755)
        snapctl = SnapCtl(executable=str(executable))
        with pytest.raises(SnapCtlError) as e:
            snapctl.run()
        assert str(e.value) == "Call to snapctl failed with error 1: fail!\n"

    def test_config_get(self, snapctl):
        output = {"foo": 123, "bar": "BAR"}
        snapctl.run.return_value = json.dumps(output)
        assert snapctl.config_get("foo", "bar") == output
        assert snapctl.run.mock_calls == [call("get", "-d", "foo", "bar")]

    def test_config_set(self, snapctl):
        snapctl.config_set({"foo.bar": 123, "baz": [1, 2, 3]})
        assert snapctl.run.mock_calls == [call("set", "foo.bar=123", "baz=[1, 2, 3]")]

    def test_config_unset(self, snapctl):
        snapctl.config_unset("foo.bar", "baz")
        assert snapctl.run.mock_calls == [call("set", "foo.bar!", "baz!")]

    def test_connection_set(self, snapctl):
        snapctl.connection_set("myplug", {"foo.bar": 123, "baz": [1, 2, 3]})
        assert snapctl.run.mock_calls == [
            call("set", ":myplug", "foo.bar=123", "baz=[1, 2, 3]")
        ]

    def test_connection_unset(self, snapctl):
        snapctl.connection_unset("myslot", "foo.bar", "baz")
        assert snapctl.run.mock_calls == [call("set", ":myslot", "foo.bar!", "baz!")]

    @pytest.mark.parametrize("code,connected", [(0, True), (1, False)])
    def test_is_connected(self, tmpdir, code, connected):
        executable = tmpdir / "snapctl"
        executable.write_text(
            dedent(
                f"""\
                #!/bin/sh
                exit {code}
                """
            ),
            "utf-8",
        )
        executable.chmod(0o755)
        snapctl = SnapCtl(executable=str(executable))
        assert snapctl.is_connected("myslot") == connected

    @pytest.mark.parametrize(
        "remote,call_args",
        [
            (False, ["get", "-d", ":myplug", "foo", "bar"]),
            (True, ["get", "-d", "--slot", ":myplug", "foo", "bar"]),
        ],
    )
    def test_plug_get(self, snapctl, remote, call_args):
        output = {"foo": 123, "bar": "BAR"}
        snapctl.run.return_value = json.dumps(output)
        assert snapctl.plug_get("myplug", "foo", "bar", remote=remote) == output
        assert snapctl.run.mock_calls == [call(*call_args)]

    @pytest.mark.parametrize(
        "remote,call_args",
        [
            (False, ["get", "-d", ":myslot", "foo", "bar"]),
            (True, ["get", "-d", "--plug", ":myslot", "foo", "bar"]),
        ],
    )
    def test_slot_get(self, snapctl, remote, call_args):
        output = {"foo": 123, "bar": "BAR"}
        snapctl.run.return_value = json.dumps(output)
        assert snapctl.slot_get("myslot", "foo", "bar", remote=remote) == output
        assert snapctl.run.mock_calls == [call(*call_args)]

    def test_start(self, snapctl):
        snapctl.start()
        assert snapctl.run.mock_calls == [call("start", "mysnap_inst")]

    def test_start_enable(self, snapctl):
        snapctl.start(enable=True)
        assert snapctl.run.mock_calls == [call("start", "--enable", "mysnap_inst")]

    def test_start_services(self, snapctl):
        snapctl.start("foo", "bar")
        assert snapctl.run.mock_calls == [
            call("start", "mysnap_inst.foo", "mysnap_inst.bar")
        ]

    def test_stop(self, snapctl):
        snapctl.stop()
        assert snapctl.run.mock_calls == [call("stop", "mysnap_inst")]

    def test_stop_enable(self, snapctl):
        snapctl.stop(disable=True)
        assert snapctl.run.mock_calls == [call("stop", "--disable", "mysnap_inst")]

    def test_stop_services(self, snapctl):
        snapctl.stop("foo", "bar")
        assert snapctl.run.mock_calls == [
            call("stop", "mysnap_inst.foo", "mysnap_inst.bar")
        ]

    def test_restart(self, snapctl):
        snapctl.restart()
        assert snapctl.run.mock_calls == [call("restart", "mysnap_inst")]

    def test_restart_enable(self, snapctl):
        snapctl.restart(reload=True)
        assert snapctl.run.mock_calls == [call("restart", "--reload", "mysnap_inst")]

    def test_restart_services(self, snapctl):
        snapctl.restart("foo", "bar")
        assert snapctl.run.mock_calls == [
            call("restart", "mysnap_inst.foo", "mysnap_inst.bar")
        ]

    def test_services(self, snapctl):
        snapctl.run.return_value = dedent(
            """\
            Service          Startup   Current   Notes
            mysnap.service1  disabled  inactive  foo,bar
            mysnap.service2  enabled   active    -
            mysnap.service3  enabled   inactive  baz
            """
        )
        assert snapctl.services() == [
            ServiceInfo(
                name="service1", enabled=False, active=False, notes=["foo", "bar"],
            ),
            ServiceInfo(name="service2", enabled=True, active=True, notes=[]),
            ServiceInfo(name="service3", enabled=True, active=False, notes=["baz"]),
        ]
        assert snapctl.run.mock_calls == [call("services", "mysnap_inst")]

    def test_services_with_services(self, snapctl):
        snapctl.run.return_value = dedent(
            """\
            Service          Startup   Current   Notes
            mysnap.service1  disabled  inactive  foo,bar
            mysnap.service3  enabled   inactive  baz
            """
        )
        assert snapctl.services("service1", "service3") == [
            ServiceInfo(
                name="service1", enabled=False, active=False, notes=["foo", "bar"],
            ),
            ServiceInfo(name="service3", enabled=True, active=False, notes=["baz"]),
        ]
        assert snapctl.run.mock_calls == [
            call("services", "mysnap_inst.service1", "mysnap_inst.service3")
        ]

    @pytest.mark.parametrize(
        "status,message,code,call_args",
        [
            (
                SnapHealthStatus.BLOCKED,
                "some message",
                "a-b-c",
                ["blocked", "some message", "--code", "a-b-c"],
            ),
            (SnapHealthStatus.OKAY, None, None, ["okay"]),
            (
                SnapHealthStatus.WAITING,
                "some message",
                None,
                ["waiting", "some message"],
            ),
        ],
    )
    def test_set_health(self, snapctl, status, message, code, call_args):
        snapctl.set_health(status, message=message, code=code)
        assert snapctl.run.mock_calls == [call("set-health", *call_args)]
