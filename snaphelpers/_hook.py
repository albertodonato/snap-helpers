from typing import (
    cast,
    List,
    NamedTuple,
)

import pkg_resources

HOOKS_ENTRY_POINT = "snaphelpers.hooks"


class Hook(NamedTuple):
    """A snap hook declared via ``entry_points``."""

    name: str
    project: str
    module: str
    import_name: str
    path: str
    exists: bool

    @classmethod
    def from_entry_point(cls, entry: pkg_resources.EntryPoint):
        try:
            entry.resolve()
        except ImportError:
            exists = False
        else:
            exists = True
        return cls(
            name=entry.name,
            project=cast(pkg_resources.Distribution, entry.dist).project_name,
            module=entry.module_name,
            import_name=entry.attrs[0],
            path=".".join(entry.attrs),
            exists=exists,
        )

    @property
    def location(self) -> str:
        """The hook location."""
        return f"{self.module}:{self.path}"

    def __str__(self):
        return f"{self.location} ({self.project})"


def get_hooks(pkg_resources=pkg_resources) -> List[Hook]:
    """Return registered snap hooks.

    Resources registred as ``snaphelpers.hooks`` in ``entry_points`` are loaded
    as hooks, based on their name.

    For example:

    .. code:: python

       setup(
           # ...
           entry_points={
               "snaphelpers.hooks"': [
                   "install = foo.bar:install_hook",
                   "configure = foo.bar:configure_hook",
               ]
           }
       )

    """
    return [
        Hook.from_entry_point(entry_point)
        for entry_point in pkg_resources.iter_entry_points(HOOKS_ENTRY_POINT)
    ]
