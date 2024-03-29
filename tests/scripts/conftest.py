from argparse import (
    ArgumentParser,
    Namespace,
)
from io import StringIO

import pytest

from snaphelpers.scripts._script import Script


class SampleScript(Script):
    def get_parser(self) -> ArgumentParser:
        parser = ArgumentParser()
        parser.add_argument("foo")
        parser.add_argument("bar")
        return parser

    def run(self, options: Namespace) -> int:
        self.options = options
        return 0


@pytest.fixture
def sample_script():
    """Return a sample Script."""
    yield SampleScript(stdout=StringIO(), stderr=StringIO())
