Implementing snap hooks
=======================

Snaps can implement hooks for different events, for instance:

- ``configure``
- ``install``
- ``pre-refresh``
- ``post-refresh``
- ...

Hooks are executable files placed under ``$SNAP/snap/hooks/``, and are executed
without parameters.

``snap-helpers`` provides some tooling to reduce boilerplate when writing
hooks. It can automatically install hook scripts for the snap it's being built in.

The snapped application can specify hook functions via ``entry_points`` in its
``setup.py``.

For instance:

.. code:: python

   setup(
       # ...
       entry_points={
           'snaphelpers.hooks': [
               'configure = testapp:configure_hook',
               'install = testapp:install_hook'
           ]
       }
   )


will register functions for the ``configure`` and ``install`` hooks.
These functions are called with a :class:`Snap` instance as argument:

.. code:: python

   def install_hook(snap: snaphelpers.Snap):
       # ...


   def configure_hook(snap: snaphelpers.Snap):
       # ...


Setting up hooks during snap build
----------------------------------

The library provides a ``snap-helpers-hook`` script that is installed in the
snap which is called hook with the hook name as argument. The script takes care
of calling the function registered for the hook (if one is defined).

A ``snap-helpers`` tool is also provided to handle the plumbing during snap
builds, and create the hook scripts, based on which hooks are defined in the
application's ``snapcraft.yaml``

All that's needed is callign ``snap-helpers write-hooks`` as part of the
application build process in the snap.

In the example above, the application would have hooks defined in its
``snapcraft.yaml`` such as (plug definitions are purely an example)

.. code:: yaml

   hooks:
     configure:
       plugs:
         - media
     install:
       plugs:
         - network


The application part just needs to ``override-build`` to call ``snap-helpers``
to set up hooks:

.. code:: yaml

   parts:
     my-app:
       # ...
       override-build: |
         set -e

         snapcraftctl build
         snap-helpers write-hooks


This will create the corresponding hook scripts in ``$SNAP/snap/hooks/``.

For a complete example, see the ``snap-helpers-testapp`` snap in the
``test-snap/`` dir.
