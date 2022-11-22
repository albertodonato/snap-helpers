from argparse import Namespace

from .._script import ScriptError


class TestScript:
    def test_run(self, sample_script):
        assert sample_script(args=["FOO", "BAR"]) == 0
        assert sample_script.options == Namespace(foo="FOO", bar="BAR")

    def test_print(self, sample_script):
        sample_script.print("out")
        sample_script.print("err", err=True)
        assert sample_script.stdout.getvalue() == "out\n"
        assert sample_script.stderr.getvalue() == "err\n"

    def test_print_endl(self, sample_script):
        sample_script.print("out", endl="")
        assert sample_script.stdout.getvalue() == "out"

    def test_error(self, sample_script):
        def run(_):
            raise ScriptError("fail", code=4)

        sample_script.run = run
        assert sample_script(args=["FOO", "BAR"]) == 4
        assert sample_script.stderr.getvalue() == "fail\n"
