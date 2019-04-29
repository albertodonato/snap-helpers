from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    Namespace,
)
import os
from pathlib import Path
from typing import (
    Mapping,
    Optional,
)

import yaml

from ._script import Script

HOOK_TEMPLATE = '''#!/bin/sh

exec "${{SNAP}}/snap/command-chain/snapcraft-runner" \
"${{SNAP}}/bin/snap-helpers-hook" "{hookname}"
'''


class SnapHelpersScript(Script):
    """Tool to perform snap-helpers tasks."""

    def __init__(self, environ: Optional[Mapping[str, str]] = None):
        if environ is None:
            environ = os.environ

    def get_parser(self) -> ArgumentParser:
        parser = ArgumentParser(
            description='Tool to perform snap-helpers tasks')
        subparsers = parser.add_subparsers(
            metavar='ACTION', dest='action', help='action to perform')
        subparsers.required = True

        subparsers.add_parser(
            'write-hooks',
            help='Write hook files',
            formatter_class=ArgumentDefaultsHelpFormatter)
        return parser

    def run(self, options: Namespace):
        action = options.action.replace('-', '_')
        getattr(self, f'_action_{action}')(options)

    def _action_write_hooks(self, options: Namespace):
        src_dir = self._ensure_env_path('SNAPCRAFT_PART_SRC')
        prime_dir = self._ensure_env_path('SNAPCRAFT_PRIME')

        with (src_dir / 'snap' / 'snapcraft.yaml').open() as fd:
            content = yaml.safe_load(fd)

        hooks = content.get('hooks')
        if not hooks:
            print('No hooks defined in the snap.')
            return

        hooks_dir = prime_dir / 'snap' / 'hooks'
        if not hooks_dir.exists():
            hooks_dir.mkdir(parents=True)

        print('Writing hook files...')
        for hookname in hooks:
            hook_file = hooks_dir / hookname
            print(f' {hookname} -> {hook_file.absolute()}')
            hook_file.write_text(HOOK_TEMPLATE.format(hookname=hookname))
            hook_file.chmod(0o755)

    def _ensure_env_path(self, name: str) -> Path:
        value = os.environ.get(name)
        if value is None:
            raise RuntimeError(f'{name} environment variable not defined')
        return Path(value)


script = SnapHelpersScript()
