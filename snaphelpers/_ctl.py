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
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
)

from ._env import SnapEnviron


class ServiceInfo(NamedTuple):
    """Information for a service in the snap."""

    name: str
    enabled: bool
    active: bool
    notes: List[str]


class SnapHealthStatus(Enum):
    """Possible values for snap health status."""

    OKAY = "okay"
    WAITING = "waiting"
    BLOCKED = "blocked"
    ERROR = "error"


class SnapCtlError(Exception):
    """A snapctl command failed."""

    returncode: int
    error: str

    def __init__(self, process: Popen):
        self.returncode = process.returncode
        self.error = cast(IO, process.stderr).read().decode("utf-8")
        super().__init__(
            f"Call to snapctl failed with error {self.returncode}: " + self.error
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
        self, executable: str = "/usr/bin/snapctl", env: Optional[SnapEnviron] = None
    ):
        if env is None:
            env = SnapEnviron()
        self._executable = executable
        self._instance_name = env.INSTANCE_NAME

    def start(self, *services: str, enable: bool = False):
        """Start all or specified services in the snap.

        :param services: a list of services defined in the snap to start.
          If not specified, all services will be started.
        :param enable: whether to also enable services at startup.

        """
        self._run_for_services("start", services, options={"enable": enable})

    def stop(self, *services: str, disable: bool = False):
        """Stop all or specified services in the snap.

        :param services: a list of services defined in the snap to stop.
          If not specified, all services will be stopped.
        :param disable: whether to also disable services at startup.

        """
        self._run_for_services("stop", services, options={"disable": disable})

    def restart(self, *services: str, reload: bool = False):
        """Restart all or specified services in the snap.

        :param services: a list of services defined in the snap to restart.
          If not specified, all services will be restarted.
        :param reload: whether to reload services if supported.

        """
        self._run_for_services("restart", services, options={"reload": reload})

    def services(self, *services: str) -> List[ServiceInfo]:
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
                notes: List[str] = []
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

    def config_get(self, *keys: str) -> Dict[str, Any]:
        """Return the snap configuration.

        :param keys: a list of config keys to return.

        """
        conf: Dict[str, Any]
        conf = json.loads(self.run("get", "-d", *keys))
        return conf

    def config_set(self, configs: Dict[str, Any]):
        """Set snap configuration.

        :param configs: a dict with configs. Keys can use dotted notation.

        """
        self.run("set", *self._set_args(configs))

    def config_unset(self, *keys: str):
        """Unset snap configuration keys.

        :param keys: config keys to unset.

        """
        self.run("set", *self._unset_args(keys))

    def connection_set(self, name: str, configs: Dict[str, Any]):
        """Set plug or slot configuration.

        :param name: the plug/slot name.
        :param configs: a dict with configs. Keys can use dotted notation.

        """
        self.run("set", f":{name}", *self._set_args(configs))

    def connection_unset(self, name: str, *keys: str):
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

    def plug_get(self, name: str, *keys: str, remote: bool = False) -> Dict[str, Any]:
        """Return plug configuration.

        :param name: the plug name.
        :param keys: a list of config keys to return.
        :param remote: if True, return configs from the remote end.

        """
        remote_type = "slot" if remote else None
        return self._connection_get(name, keys, remote_type=remote_type)

    def slot_get(self, name: str, *keys: str, remote: bool = False) -> Dict[str, Any]:
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
        message: Optional[str] = None,
        code: Optional[str] = None,
    ):
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

    def run(self, *args: str) -> str:
        """Execute the command and return its output.

        :param args: command args.

        """
        process = Popen([self._executable, *args], stdout=PIPE, stderr=PIPE)
        process.wait()
        if process.returncode:
            raise SnapCtlError(process)
        output: bytes = cast(IO, process.stdout).read()
        return output.decode("utf-8")

    def _run_for_services(
        self,
        cmd: str,
        services: Sequence[str],
        options: Optional[Dict[str, bool]] = None,
    ) -> str:
        opts: List[str] = []
        if options:
            opts = [f"--{option}" for option, value in options.items() if value]
        if services:
            service_names = [f"{self._instance_name}.{service}" for service in services]
        else:
            service_names = [self._instance_name]
        return self.run(cmd, *opts, *service_names)

    def _set_args(self, configs: Dict[str, Any]) -> List[str]:
        return [f"{key}={json.dumps(value)}" for key, value in configs.items()]

    def _unset_args(self, configs: Tuple[str, ...]) -> List[str]:
        return [f"{key}!" for key in configs]

    def _connection_get(
        self,
        name: str,
        keys: Tuple[str, ...],
        remote_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        args = ["get", "-d"]
        if remote_type:
            args.append(f"--{remote_type}")
        args.append(f":{name}")
        args.extend(keys)
        conf: Dict[str, Any]
        conf = json.loads(self.run(*args))
        return conf
