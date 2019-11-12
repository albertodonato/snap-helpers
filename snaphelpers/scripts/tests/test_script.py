from argparse import (
    ArgumentParser,
    Namespace,
)

from .._script import Script


class SampleScript(Script):
    def get_parser(self):
        parser = ArgumentParser()
        parser.add_argument("foo")
        parser.add_argument("bar")
        return parser

    def run(self, options: Namespace):
        self.options = options


class TestScript:
    def test_run(self):
        script = SampleScript()
        script(args=["FOO", "BAR"])
        assert script.options == Namespace(foo="FOO", bar="BAR")
