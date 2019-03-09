from ._hooks import (
    configure_hook,
    install_hook,
)
from ._service import Service


__all__ = ['configure_hook', 'install_hook', 'service1', 'service2']

service1 = Service('service1')
service2 = Service('service2')
