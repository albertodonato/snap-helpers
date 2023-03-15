Implementing snap hooks
=======================

Snaps can implement hooks for different events, for instance:

* ``configure``
* ``install``
* ``pre-refresh``
* ``post-refresh``
* ...

Hooks are executable files placed under ``$SNAP/snap/hooks/``, and are executed
without parameters.

``snap-helpers`` provides some tooling to reduce boilerplate when writing
hooks. It can automatically install hook scripts for the snap it's being built
in.

The snapped application can specify hook functions via entry-points in package
metadata, under the ``snaphelpers.hook`` key.

For instance, in ``pyproject.toml``:

.. code:: toml

   [project.entry-points."snaphelpers.hooks"]
   configure = "testapp:configure_hook"
   install = "testapp:install_hook"

will allow registering functions for the ``configure`` and ``install`` hooks.
These functions are called with a :class:`.Snap` instance as argument:

.. code:: python

   def install_hook(snap: snaphelpers.Snap):
       # ...


   def configure_hook(snap: snaphelpers.Snap):
       # ...


Setting up hooks during snap build
----------------------------------

The library provides a ``snap-helpers`` command which can be used during snap
builds to generate the hook scripts.

All that's needed is calling ``snap-helpers write-hooks`` as part of the
application build process in the snap.

The tool looks up Python packages installed in the snap that define
``snaphelper.hooks``, and creates hook scripts under ``$SNAP/snap/hooks`` for
each one of them.

The application part just needs to ``override-build`` to call ``snap-helpers``
to set up hooks:

.. code:: yaml

   parts:
     my-app:
       plugin: python
       # other part configurations
       python-packages:
         - snap-helpers
         # ... other dependencies
       override-build: |
         craftctl default  # perform the regular build process
         snap-helpers write-hooks


For a complete example, see the ``snap-helpers-testapp`` part in the sna
definition under the ``test-snap/`` directory.
