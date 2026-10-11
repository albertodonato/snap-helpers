# Copyright Alberto Donato 2019, 2026
# SPDX-License-Identifier: LGPL-3.0-or-later

import pytest

from snaphelpers import Snap

SERVICES = {"service1", "service2"}


@pytest.mark.parametrize("service", SERVICES)
def test_service(snap: Snap, service: str) -> None:
    services = snap.services.list()
    assert service in services
    assert services[service].enabled
    assert services[service].active
