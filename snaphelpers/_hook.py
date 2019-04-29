from typing import (
    Callable,
    Dict,
)

import pkg_resources

from ._snap import Snap

Hook = Callable[[Snap], None]


def get_hooks(pkg_resources=pkg_resources) -> Dict[str, Hook]:
    """Return registered snap hooks.

    Resources registreed in setup.py as `snaphelpers.hooks` are loaded as
    hooks, based on their name.

    For example:

    .. code::

       setup(
           # ...
           entry_points={
               'snaphelpers.hooks': [
                   'install = 'foo.bar:install_hook',
                   'configure = 'foo.bar:configure_hook'
               ]
           }
       )

    """
    return {
        entry.name: entry.load()
        for entry in pkg_resources.iter_entry_points('snaphelpers.hooks')
    }
