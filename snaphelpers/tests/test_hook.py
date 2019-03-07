from typing import (
    Callable,
    NamedTuple,
)

import pytest

from .._hook import get_hooks


class MockEntryPoint(NamedTuple):

    name: str
    load: Callable


@pytest.fixture
def hook_calls():
    yield []


@pytest.fixture
def entry_points(hook_calls):

    def make_load(name):

        def load():
            hook_calls.append(name)
            return f'loaded-{name}'

        return load

    yield [
        MockEntryPoint(name='install', load=make_load('install')),
        MockEntryPoint(name='configure', load=make_load('configure'))
    ]


@pytest.fixture
def mock_pkg_resources(mocker, entry_points):
    pkg_resources = mocker.Mock()
    pkg_resources.iter_entry_points.return_value = iter(entry_points)
    yield pkg_resources


class TestGetHooks:

    def test_hooks(self, mock_pkg_resources, hook_calls):
        assert get_hooks(pkg_resources=mock_pkg_resources) == {
            'configure': 'loaded-configure',
            'install': 'loaded-install'
        }
        assert hook_calls == ['install', 'configure']
