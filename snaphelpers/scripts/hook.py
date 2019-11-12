from argparse import (
    ArgumentParser,
    Namespace,
)

from .._hook import get_hooks
from .._snap import Snap
from ._script import Script


class HookScript(Script):
    """A wrapper script to call hooks registered via :data:`pkg_resources`."""

    def get_parser(self) -> ArgumentParser:
        parser = ArgumentParser(
            description="Run the specified hook registered via pkg_resources"
        )
        parser.add_argument("hook", help="name of the hook to run")
        return parser

    def run(self, options: Namespace):
        hooks = get_hooks()
        hook = hooks.get(options.hook)
        if hook:
            hook(Snap())


script = HookScript()
