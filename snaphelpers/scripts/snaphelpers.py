from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    Namespace,
)
import os
from pathlib import Path
from textwrap import dedent
from typing import (
    Mapping,
    NamedTuple,
    Optional,
)

from .._hook import (
    get_hooks,
    HOOKS_ENTRY_POINT,
)
from ._script import Script


class HookScript(NamedTuple):
    """A hook script."""

    name: str
    hooks_dir: Path

    def render(self) -> str:
        """Return the rendered script."""
        return dedent(
            f"""\
            #!/bin/sh

            exec "${{SNAP}}/snap/command-chain/snapcraft-runner" \\
                "${{SNAP}}/bin/snap-helpers-hook" "{self.name}"
            """
        )

    def path(self) -> Path:
        """Return the path of f the script."""
        return self.hooks_dir / self.name

    def write(self):
        """Write the hook script to file."""
        path = self.path()
        path.write_text(self.render())
        path.chmod(0o755)


class SnapHelpersScript(Script):
    """Tool to perform snap-helpers tasks."""

    def __init__(self, environ: Optional[Mapping[str, str]] = None):
        if environ is None:
            environ = os.environ

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
            "-X",
            "--exclude",
            nargs="*",
            default=[],
            help="don't create scripts for specified hooks (even if present in snapcraft.yaml)",
        )
        return parser

    def run(self, options: Namespace):
        action = options.action.replace("-", "_")
        getattr(self, f"_action_{action}")(options)

    def _action_write_hooks(self, options: Namespace):
        prime_dir = self._ensure_env_path("SNAPCRAFT_PRIME")

        hooks = list(get_hooks())
        if not hooks:
            print(
                "No hooks defined in the snap.\n"
                f'Hooks must be defined in the "{HOOKS_ENTRY_POINT}" '
                "section of entry points."
            )
            return

        hooks_dir = prime_dir / "snap" / "hooks"
        if not hooks_dir.exists():
            hooks_dir.mkdir(parents=True)

        unknown_hooks = set(options.exclude).difference(hooks)
        if unknown_hooks:
            hooks_list = ", ".join(sorted(unknown_hooks))
            raise RuntimeError(f"The following hook(s) are not defined: {hooks_list}")
        print("Writing hook files...")
        for hookname in hooks:
            if hookname in options.exclude:
                continue
            hook_script = HookScript(hookname, hooks_dir)
            print(f" {hookname} -> {hook_script.path().absolute()}")
            hook_script.write()

    def _ensure_env_path(self, name: str) -> Path:
        value = os.environ.get(name)
        if value is None:
            raise RuntimeError(f"{name} environment variable not defined")
        return Path(value)


script = SnapHelpersScript()
