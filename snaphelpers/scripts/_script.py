from abc import (
    ABC,
    abstractmethod,
)
from argparse import (
    ArgumentParser,
    Namespace,
)
import sys
from typing import (
    IO,
    List,
    Optional,
)


class ScriptError(Exception):
    """Raised to exit the script with a message and error code."""

    def __init__(self, message: str, code: int = 1):
        super().__init__(message)
        self.code = code


class Script(ABC):
    """A Script."""

    def __init__(self, stdout: IO = sys.stdout, stderr: IO = sys.stderr):
        self.stdout = stdout
        self.stderr = stderr

    @abstractmethod
    def get_parser(self) -> ArgumentParser:
        """Return a parser for the script.

        Subclasses must implement this method.

        """

    @abstractmethod
    def run(self, options: Namespace) -> Optional[int]:
        """Run the script

        Subclasses must implement this method.

        """

    def __call__(self, args: Optional[List[str]] = None) -> Optional[int]:
        parser = self.get_parser()
        opts = parser.parse_args(args=args)
        try:
            return self.run(opts)
        except ScriptError as error:
            self.print(str(error), err=True)
            return error.code

    def print(self, message: str, err: bool = False, endl: str = "\n") -> None:
        """Print a message to stdout or stderr."""
        stream = self.stderr if err else self.stdout
        stream.write(message + endl)
