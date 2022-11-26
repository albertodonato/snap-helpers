from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    Namespace,
)
from collections import defaultdict
from operator import attrgetter
import os
from pathlib import Path
from textwrap import dedent
from typing import (
    Dict,
    List,
)

from .._hook import (
    get_hooks,
    Hook,
    HOOKS_ENTRY_POINT,
)
from ._script import (
    Script,
    ScriptError,
)


class HookScript:
    """A hook script to be rendered."""

    def __init__(self, hook: Hook):
        self.hook = hook

    def render(self) -> str:
        """Return the rendered script."""
        return dedent(
            f"""\
            #!/usr/bin/env python3
            # -*- coding: utf-8 -*-

            import sys

            from snaphelpers import Snap
            from {self.hook.module} import {self.hook.import_name}

            sys.exit({self.hook.path}(Snap()))
            """
        )

    def write(self, hooks_dir: Path):
        """Write the hook script in the specified directory."""
        path = hooks_dir / self.hook.name
        path.write_text(self.render())
        path.chmod(0o755)


class SnapHelpersScript(Script):
    """Tool to perform snap-helpers tasks."""

    def get_parser(self) -> ArgumentParser:
        parser = ArgumentParser(description="Tool to perform snap-helpers tasks")
        subparsers = parser.add_subparsers(
            metavar="ACTION", dest="action", help="action to perform"
        )
        subparsers.required = True

        write_hooks = subparsers.add_parser(
            "write-hooks",
            help="Write hook files",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        write_hooks.add_argument(
            "--prime-dir", help="snap prime directory (default from snacraft env var)"
        )
        return parser

    def run(self, options: Namespace):
        action = options.action.replace("-", "_")
        getattr(self, f"_action_{action}")(options)

    def _action_write_hooks(self, options: Namespace):
        if options.prime_dir:
            prime_dir = Path(options.prime_dir)
        else:
            prime_dir = self._ensure_env_path("CRAFT_PRIME", fallback="SNAPCRAFT_PRIME")

        hooks = sorted(get_hooks(), key=attrgetter("name"))
        self._validate_hooks(hooks)
        if not hooks:
            self.print(
                "No hooks defined in the snap.\n"
                f'Hooks must be defined in the "{HOOKS_ENTRY_POINT}" '
                "section of entry points."
            )
            return

        hooks_dir = prime_dir / "snap" / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)

        self.print(f"Writing hook files to {hooks_dir.absolute()}")
        for hook in hooks:
            hook_script = HookScript(hook)
            self.print(f" {hook.name}: {hook} ({hook.project})")
            hook_script.write(hooks_dir)

    def _ensure_env_path(self, name: str, fallback: str = "") -> Path:
        value = os.environ.get(name)
        if value is None and fallback:
            value = os.environ.get(fallback)
        if value is None:
            raise ScriptError(f"{name} environment variable not defined")
        return Path(value)

    def _validate_hooks(self, hooks: List[Hook]):
        hooks_by_name: Dict[str, List[Hook]] = defaultdict(list)
        not_found_hooks = []
        for hook in hooks:
            if not hook.exists:
                not_found_hooks.append(hook)
            hooks_by_name[hook.name].append(hook)

        # check for duplicated entries
        duplicated = sorted(
            name for name, hooks in hooks_by_name.items() if len(hooks) > 1
        )
        if duplicated:
            message = ["Multiple definitions found for hook(s):"]
            for name in duplicated:
                message.append(f"- {name}")
                message.extend(f"    {hook}" for hook in sorted(hooks_by_name[name]))
            raise ScriptError("\n".join(message))

        # check that they exist
        if not_found_hooks:
            message = ["Hook function(s) not found:"]
            for hook in not_found_hooks:
                message.append(f"- {hook}")
            raise ScriptError("\n".join(message))


script = SnapHelpersScript()
