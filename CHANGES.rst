v0.4.2 - 2023-08-06
===================

- Rebuild to fix version


v0.4.1 - 2023-08-06
===================

- Add missing py.typed marker to package
- [docs] Fix ReadTheDocs setup


v0.4.0 - 2023-07-16
===================

- Add support for ``snapctl refresh``.
- Add support for ``snapctl system-mode``.
- Add option to make fail ``write-hooks`` fail when no hook is found.
- Drop support for Python 3.6 and ``core18``. (#13)
- Replace ``pkg_resources`` with ``importlib.metadata``. (#16)
- Rework project setup, move to ``pyproject.toml`` only.
- [gh] Switch to Codecov action.


v0.3.2 - 2023-01-14
===================

- Add ``SnapConfig.unset``.
- Rework the test snap and Add integration tests.
- [gh] Add actions for running integration tests against supported bases.


v0.3.1 - 2022-12-03
===================

- Replace shell script for hooks, direcly generate Python scripts instead.
- Add ``SnapPaths.real_home`` path.
- [snap] Enable colors in IPython configuration.


v0.3.0 - 2022-11-19
===================

- Add support in ``SnapCtl`` for interacting with plugs and slots.
- Support ``core22``-based snaps.
- [snap] Rebase snap on ``core22``.
- Add integration tests.


v0.2.0 - 2019-11-20
===================

- Provide access to metadata files (``manifest.yaml``, ``snap.yaml`` and
  ``snapcraft.yaml``).
- Read list of hooks from ``entry_points`` instead of ``snapcraft.yaml``
  (there's no need to declare all hooks in this file anymore for
  ``snap-helpers`` to find them).


v0.1.6 - 2019-09-18
===================

- Support setting snap health status.


v0.1.5 - 2019-04-29
===================

- Lint fixes.


v0.1.4 - 2019-04-29
===================

- Revert ``Snap.revision`` change as it can contain letters (e.g. ``x1``).


v0.1.3 - 2019-04-29
===================

- Change ``Snap.revision`` to be an ``int``, so it can be compared.


v0.1.2 - 2019-03-14
===================

- Print out hooks being created in ``snap-helpers write-hooks``.


v0.1.1 - 2019-03-12
===================

- Add ``SnapConfigOptions.get()`` to retrieve a single option with a default


v0.1.0 - 2019-03-10
===================

- Support for listing and managing Snap services
- Improvement to the ``snap-helper-testapp`` sample snap


v0.0.1 - 2019-03-09
===================

- Initial release
