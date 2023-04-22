from __future__ import annotations  # for subscritable Popen type

from enum import Enum
import json
import re
from subprocess import (
    PIPE,
    Popen,
)
from typing import (
    Any,
    cast,
    Dict,
    IO,
    NamedTuple,
    Sequence,
)

import yaml

from ._env import SnapEnviron


class ServiceInfo(NamedTuple):
    """Information for a service in the snap."""

    #: Name of the service
    name: str
    #: Whether the service is enabled
    enabled: bool
    #: Whether the service is active
    active: bool
    #: Additional metadata about the service
    notes: list[str]


class SnapHealthStatus(Enum):
    """Possible values for snap health status."""

    OKAY = "okay"
    WAITING = "waiting"
    BLOCKED = "blocked"
    ERROR = "error"


class SnapCtlError(Exception):
    """A snapctl command failed."""

    #: The process return code
    returncode: int
    #: The error message
    error: str

    def __init__(self, process: Popen[bytes]):
        self.returncode = process.returncode
        self.error = cast(IO[bytes], process.stderr).read().decode("utf-8")
        super().__init__(
            f"Call to snapctl failed with error {self.returncode}: "
            + self.error
        )


class SnapCtl:
    """Run the :data:`snapctl` command."""

    _SERVICE_RE = re.compile(
        r"[^.]+\.(?P<name>\S+)\s+"
        r"(?P<startup>\S+)\s+"
        r"(?P<current>\S+)\s+"
        r"(?P<notes>\S+)"
    )

    def __init__(
        self,
        executable: str = "/usr/bin/snapctl",
        env: SnapEnviron | None = None,
    ):
        if env is None:
            env = SnapEnviron()
        self._executable = executable
        self._instance_name = env.INSTANCE_NAME

    def start(self, *services: str, enable: bool = False) -> None:
        """Start all or specified services in the snap.

        :param services: a list of services defined in the snap to start.
          If not specified, all services will be started.
        :param enable: whether to also enable services at startup.

        """
        self._run_for_services("start", services, options={"enable": enable})

    def stop(self, *services: str, disable: bool = False) -> None:
        """Stop all or specified services in the snap.

        :param services: a list of services defined in the snap to stop.
          If not specified, all services will be stopped.
        :param disable: whether to also disable services at startup.

        """
        self._run_for_services("stop", services, options={"disable": disable})

    def restart(self, *services: str, reload: bool = False) -> None:
        """Restart all or specified services in the snap.

        :param services: a list of services defined in the snap to restart.
          If not specified, all services will be restarted.
        :param reload: whether to reload services if supported.

        """
        self._run_for_services("restart", services, options={"reload": reload})

    def services(self, *services: str) -> list[ServiceInfo]:
        """Return info about services in the snap.

        :param services: a list of services to return info for.
          If not specified, all services are returned.

        """
        lines = self._run_for_services("services", services)
        service_infos = []
        # skip header
        for line in lines.splitlines()[1:]:
            match = self._SERVICE_RE.match(line)
            if match:
                info = match.groupdict()
                notes: list[str] = []
                if info["notes"] != "-":
                    notes = info["notes"].split(",")
                service_infos.append(
                    ServiceInfo(
                        name=info["name"],
                        enabled=info["startup"] == "enabled",
                        active=info["current"] == "active",
                        notes=notes,
                    )
                )
        return service_infos

    def config_get(self, *keys: str) -> dict[str, Any]:
        """Return the snap configuration.

        :param keys: a list of config keys to return.

        """
        conf: dict[str, Any]
        conf = json.loads(self.run("get", "-d", *keys))
        return conf

    def config_set(self, configs: dict[str, Any]) -> None:
        """Set snap configuration.

        :param configs: a dict with configs. Keys can use dotted notation.

        """
        self.run("set", *self._set_args(configs))

    def config_unset(self, *keys: str) -> None:
        """Unset snap configuration keys.

        :param keys: config keys to unset.

        """
        self.run("set", *self._unset_args(keys))

    def connection_set(self, name: str, configs: dict[str, Any]) -> None:
        """Set plug or slot configuration.

        :param name: the plug/slot name.
        :param configs: a dict with configs. Keys can use dotted notation.

        """
        self.run("set", f":{name}", *self._set_args(configs))

    def connection_unset(self, name: str, *keys: str) -> None:
        """Unset plug or slot configuration.

        :param name: the plug/slot name.
        :param keys: keys to unset. Dotted notation can be used.

        """
        self.run("set", f":{name}", *self._unset_args(keys))

    def is_connected(self, name: str) -> bool:
        """Return whether a plug or slot is connected.

        :param name: the plug or slot name.

        """
        try:
            self.run("is-connected", name)
        except SnapCtlError:
            return False
        return True

    def plug_get(
        self, name: str, *keys: str, remote: bool = False
    ) -> dict[str, Any]:
        """Return plug configuration.

        :param name: the plug name.
        :param keys: a list of config keys to return.
        :param remote: if True, return configs from the remote end.

        """
        remote_type = "slot" if remote else None
        return self._connection_get(name, keys, remote_type=remote_type)

    def slot_get(
        self, name: str, *keys: str, remote: bool = False
    ) -> dict[str, Any]:
        """Return slot configuration.

        :param name: the slot name.
        :param keys: a list of config keys to return.
        :param remote: if True, return configs from the remote end.

        """
        remote_type = "plug" if remote else None
        return self._connection_get(name, keys, remote_type=remote_type)

    def set_health(
        self,
        status: SnapHealthStatus,
        message: str | None = None,
        code: str | None = None,
    ) -> None:
        """Set snap health.

        :param status: the status to set
        :param message: an optional message string
        :param code: an optional code string

        """
        args = [status.value]
        if message is not None:
            args.append(message)
        if code is not None:
            args.extend(["--code", code])
        self.run("set-health", *args)

    def system_mode(self) -> dict[str, Any]:
        """Return info on the device current system mode."""
        mode: dict[str, Any] = yaml.safe_load(self.run("system-mode"))
        return mode

    def refresh(self, action: str | None = None) -> dict[str, Any]:
        """Return refresh state of the snap, optionally requesting an action.

        To perform actions, the snap must have the ``snap-refresh-control``
        interface.

        :param action: Optional refresh action to perform, either ``proceed``
          or ``hold``.

        """
        args = ["--pending"]
        if action:
            args.append(f"--{action}")
        return cast(Dict[str, Any], yaml.safe_load(self.run("refresh", *args)))

    def run(self, *args: str) -> str:
        """Execute the command and return its output.

        :param args: command args.

        """
        process = Popen([self._executable, *args], stdout=PIPE, stderr=PIPE)
        process.wait()
        if process.returncode:
            raise SnapCtlError(process)
        output: bytes = cast(IO[bytes], process.stdout).read()
        return output.decode("utf-8")

    def _run_for_services(
        self,
        cmd: str,
        services: Sequence[str],
        options: dict[str, bool] | None = None,
    ) -> str:
        opts: list[str] = []
        if options:
            opts = [
                f"--{option}" for option, value in options.items() if value
            ]
        if services:
            service_names = [
                f"{self._instance_name}.{service}" for service in services
            ]
        else:
            service_names = [self._instance_name]
        return self.run(cmd, *opts, *service_names)

    def _set_args(self, configs: dict[str, Any]) -> list[str]:
        return [f"{key}={json.dumps(value)}" for key, value in configs.items()]

    def _unset_args(self, configs: tuple[str, ...]) -> list[str]:
        return [f"{key}!" for key in configs]

    def _connection_get(
        self,
        name: str,
        keys: tuple[str, ...],
        remote_type: str | None = None,
    ) -> dict[str, Any]:
        args = ["get", "-d"]
        if remote_type:
            args.append(f"--{remote_type}")
        args.append(f":{name}")
        args.extend(keys)
        conf: dict[str, Any] = json.loads(self.run(*args))
        return conf
