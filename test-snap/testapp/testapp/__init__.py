# Copyright Alberto Donato 2019, 2026
# SPDX-License-Identifier: LGPL-3.0-or-later

from ._hooks import (
    configure_hook,
    install_hook,
)
from ._service import Service

__all__ = ["configure_hook", "install_hook", "service1", "service2"]

service1 = Service("service1")
service2 = Service("service2")
