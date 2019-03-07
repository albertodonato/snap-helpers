from abc import (
    ABC,
    abstractmethod,
)
from argparse import (
    ArgumentParser,
    Namespace,
)
from typing import (
    List,
    Optional,
)


class Script(ABC):
    """A Script."""

    @abstractmethod
    def get_parser(self) -> ArgumentParser:
        """Return a parser for the script.

        Subclasses must implement this method.
        """

    @abstractmethod
    def run(self, options: Namespace):
        """Run the script

        Subclasses must implement this method.

        """

    def __call__(self, args: Optional[List[str]] = None):
        parser = self.get_parser()
        opts = parser.parse_args(args=args)
        self.run(opts)
