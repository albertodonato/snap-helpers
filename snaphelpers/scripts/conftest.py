from argparse import (
    ArgumentParser,
    Namespace,
)
from io import StringIO

import pytest

from ._script import Script


class SampleScript(Script):
    def get_parser(self):
        parser = ArgumentParser()
        parser.add_argument("foo")
        parser.add_argument("bar")
        return parser

    def run(self, options: Namespace):
        self.options = options
        return 0


@pytest.fixture
def sample_script():
    """Return a sample Script."""
    yield SampleScript(stdout=StringIO(), stderr=StringIO())
