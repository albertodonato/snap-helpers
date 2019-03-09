import pytest

from .. import hook
from ..hook import HookScript


@pytest.fixture
def hook_calls():
    yield []


@pytest.fixture
def hooks(hook_calls):
    yield {
        'configure': lambda snap: hook_calls.append('configure'),
        'install': lambda snap: hook_calls.append('install')
    }


@pytest.fixture
def mock_get_hooks(mocker, hooks):
    mocker.patch.object(hook, 'get_hooks', lambda: hooks)


@pytest.mark.usefixtures('snap_apply_env', 'mock_get_hooks')
class TestHookScript:

    def test_run_hook(self, hook_calls):
        script = HookScript()
        script(args=['install'])
        script(args=['configure'])
        assert hook_calls == ['install', 'configure']

    def test_no_hook(self, hooks, hook_calls):
        hooks.pop('install')
        script = HookScript()
        script(args=['install'])
        assert hook_calls == []
