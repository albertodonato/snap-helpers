import json
import re
from subprocess import check_output
from typing import (
    Any,
    Dict,
    Iterable,
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


class SnapCtl:
    """Run the :data:`snapctl` command."""

    _SERVICE_RE = re.compile(
        r'[^.]+\.(?P<name>\S+)\s+'
        r'(?P<startup>\S+)\s+'
        r'(?P<current>\S+)\s+'
        r'(?P<notes>\S+)')

    def __init__(
            self,
            executable: str = '/usr/bin/snapctl',
            env: Optional[SnapEnviron] = None):
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
        args = ['start']
        if enable:
            args.append('--enable')
        if services:
            args.extend(self._service_names(services))
        self._run(*args)

    def stop(self, *services: str, disable: bool = False):
        """Stop all or specified services in the snap.

        :param services: a list of services defined in the snap to stop..
          If not specified, all services will be stopped.
        :param disable: whether to also disable services at startup.

        """
        args = ['stop']
        if disable:
            args.append('--disable')
        if services:
            args.extend(self._service_names(services))
        self._run(*args)

    def services(self) -> List[ServiceInfo]:
        """Return info about services in the snap."""
        lines = self._run('services').splitlines()[1:]
        service_infos = []
        for line in lines:
            match = self._SERVICE_RE.match(line)
            if match:
                info = match.groupdict()
                notes: List[str] = []
                if info['notes'] != '-':
                    notes = info['notes'].split(',')
                service_infos.append(
                    ServiceInfo(
                        name=info['name'],
                        enabled=info['startup'] == 'enabled',
                        active=info['current'] == 'active',
                        notes=notes))
        return service_infos

    def get(self, *keys: str) -> Dict[str, Any]:
        """Return the snap config.

        :param keys: a list of config keys to return.

        """
        conf: Dict[str, Any]
        conf = json.loads(self._run('get', '-d', *keys))
        return conf

    def set(self, configs: Dict[str, Any]):
        """Set snap configs.

        :param configs: a dict with configs. Keys can use dotted notation.

        """
        args = [f'{key}={json.dumps(value)}' for key, value in configs.items()]
        self._run('set', *args)

    def _run(self, *args: str) -> str:
        """Execute the command return its output.

        ":param args: command args.

        """
        output: bytes = check_output([self._executable, *args])
        return output.decode('utf-8')

    def _service_names(self, services: Sequence[str]) -> Iterable[str]:
        return (f'{self._instance_name}.{service}' for service in services)
