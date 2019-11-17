from enum import Enum
import json
import re
from subprocess import (
    PIPE,
    Popen,
)
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Sequence,
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
        self.error = process.stderr.read().decode("utf-8")
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
        """Return the snap config.

        :param keys: a list of config keys to return.

        """
        conf: Dict[str, Any]
        conf = json.loads(self.run("get", "-d", *keys))
        return conf

    def config_set(self, configs: Dict[str, Any]):
        """Set snap configs.

        :param configs: a dict with configs. Keys can use dotted notation.

        """
        args = [f"{key}={json.dumps(value)}" for key, value in configs.items()]
        self.run("set", *args)

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
        output: bytes = process.stdout.read()
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
