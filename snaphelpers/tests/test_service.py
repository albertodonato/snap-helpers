from textwrap import dedent
from unittest.mock import call

import pytest

from .._ctl import (
    ServiceInfo,
    SnapCtl,
)
from .._service import (
    SnapService,
    SnapServices,
)


@pytest.fixture
def snap_service_status_output(snapctl):
    yield dedent(
        f'''\
        Service               Startup   Current   Notes
        mysnap_inst.serv1     disabled  inactive  foo,bar
        ''')


class TestSnapService:

    def test_attrs(self, snapctl):
        info = ServiceInfo(
            name='serv1', enabled=True, active=False, notes=['foo', 'bar'])
        service = SnapService(info, snapctl=snapctl)
        assert service.name == 'serv1'
        assert service.enabled
        assert not service.active
        assert service.notes == ['foo', 'bar']

    def test_eq(self, snapctl):
        info = ServiceInfo(
            name='serv1', enabled=True, active=False, notes=['foo', 'bar'])
        assert (
            SnapService(info,
                        snapctl=snapctl) == SnapService(info, snapctl=snapctl))

    def test_eq_other_info(self, snapctl):
        info1 = ServiceInfo(
            name='serv1', enabled=True, active=False, notes=['foo', 'bar'])
        info2 = ServiceInfo(
            name='serv2', enabled=True, active=False, notes=['foo', 'bar'])
        assert (
            SnapService(info1, snapctl=snapctl) != SnapService(
                info2, snapctl=snapctl))

    def test_eq_other_snapctl(self, snapctl):
        info = ServiceInfo(
            name='serv1', enabled=True, active=False, notes=['foo', 'bar'])
        assert (
            SnapService(info, snapctl=snapctl) != SnapService(
                info, snapctl=SnapCtl()))

    @pytest.mark.parametrize('action', ['start', 'stop', 'restart'])
    def test_actions(self, action, snapctl, snap_service_status_output):
        snapctl.run.side_effect = ['', snap_service_status_output]
        info = ServiceInfo(name='serv1', enabled=True, active=True, notes=[])
        service = SnapService(info, snapctl=snapctl)
        getattr(service, action)()
        assert snapctl.run.mock_calls == [
            call(action, 'mysnap_inst.serv1'),
            call('services', 'mysnap_inst.serv1')
        ]

    @pytest.mark.parametrize(
        'action, option',
        [('start', 'enable'), ('stop', 'disable'), ('restart', 'reload')])
    def test_actions_with_options(
            self, action, option, snapctl, snap_service_status_output):
        snapctl.run.side_effect = ['', snap_service_status_output]
        info = ServiceInfo(name='serv1', enabled=True, active=True, notes=[])
        service = SnapService(info, snapctl=snapctl)
        getattr(service, action)(**{option: True})
        assert snapctl.run.mock_calls == [
            call(action, f'--{option}', 'mysnap_inst.serv1'),
            call('services', 'mysnap_inst.serv1')
        ]

    def test_refresh_status(self, snapctl, snap_service_status_output):
        snapctl.run.return_value = snap_service_status_output
        info = ServiceInfo(name='serv1', enabled=True, active=True, notes=[])
        service = SnapService(info, snapctl=snapctl)
        service.refresh_status()
        assert not service.enabled
        assert not service.active
        assert service.notes == ['foo', 'bar']


class TestSnapServices:

    @pytest.mark.parametrize('action', ['start', 'stop', 'restart'])
    def test_actions(self, action, snapctl):
        services = SnapServices(snapctl=snapctl)
        getattr(services, action)()
        assert snapctl.run.mock_calls == [call(action, 'mysnap_inst')]

    def test_list(self, fake_snapctl):
        services = SnapServices(snapctl=fake_snapctl)
        info1 = ServiceInfo(
            name='serv1', enabled=True, active=False, notes=['foo'])
        info2 = ServiceInfo(
            name='serv2', enabled=False, active=True, notes=['bar'])
        fake_snapctl._services = [info1, info2]
        assert services.list() == {
            'serv1': SnapService(info1, snapctl=fake_snapctl),
            'serv2': SnapService(info2, snapctl=fake_snapctl)
        }
