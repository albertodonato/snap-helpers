snap-helpers - Interact with the Snap system within a Snap
==========================================================

|Latest Version| |Build Status| |Coverage Status| |Documentation|


A Python library to interact with snap configuration and properties from inside a snap.

It exposes a top-level ``snaphelpers.Snap`` object which provides access to:

- snap details:

  .. code:: python

     >>> snap = snaphelpers.Snap()
     >>> snap.name
     'testapp'
     >>> snap.instance_name
     'testapp'
     >>> snap.version
     '0+git.fdf80cd'
     >>> snap.revision
     'x1'

- paths:

  .. code:: python

     >>> snap.paths.common
     PosixPath('/var/snap/testapp/common')
     >>> snap.paths.data
     PosixPath('/var/snap/testapp/x1')
     >>> snap.paths.snap
     PosixPath('/snap/testapp/x1')
     >>> snap.paths.user_common
     PosixPath('/home/ack/snap/testapp/common')
     >>> snap.paths.user_data
     PosixPath('/home/ack/snap/testapp/x1')

- snap-related environment variables:

  .. code:: python

     >>> pprint.pprint(dict(snap.environ))
     {'ARCH': 'amd64',
      'COMMON': '/var/snap/testapp/common',
      'CONTEXT': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890',
      'COOKIE': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890',
      'DATA': '/var/snap/testapp/x1',
      'INSTANCE_KEY': '',
      'INSTANCE_NAME': 'testapp',
      'LIBRARY_PATH': '/var/lib/snapd/lib/gl:/var/lib/snapd/lib/gl32:/var/lib/snapd/void',
      'NAME': 'testapp',
      'REEXEC': '',
      'REVISION': 'x1',
      'SNAP': '/snap/testapp/x1',
      'USER_COMMON': '/home/ack/snap/testapp/common',
      'USER_DATA': '/home/ack/snap/testapp/x1',
      'VERSION': '0+git.fdf80cd'}
     >>> snap.environ.ARCH
     'amd64'

- configuration options:

  .. code:: python

     >>> snap.config.set({'foo.bar': 'baz', 'asdf': 3})  # this needs to be run as root
     >>> options = snap.config.get_options('foo', 'asdf')
     >>> options['foo']
     {'bar': 'baz'}
     >>> options['foo.bar']
     'baz'
     >>> options['asdf']
     3
     >>> options.as_dict()
     {'asdf': 3, 'foo': {'bar': 'baz'}}

- setting snap health status, along with message and optional status code:

  .. code:: python

     >>> snap.health.okay()
     >>> snap.health.waiting('foo must happen first', code='wait-foo')

  Health status (when different from ``okay``) is visible from the ``snap``
  CLI::

    $ snap info snap-helpers
    name:    snap-helpers
    summary: Test snap for snap-helpers
    health:
      status:  waiting
      message: foo must happen first
      code:    wait-foo
      checked: today at 16:23 CEST

- content of snap metadata files such as:

  - ``snap/metadata.yaml``
  - ``meta/snap.yaml``
  - ``snap/snapcraft.yaml``

  These can be accessed as follows:

  .. code:: python

     >>> snap.metadata_files.snap
     SnapMetadataFile(/snap/snap-helpers/x3/meta/snap.yaml)
     >>> pprint(dict(snap.metadata_files.snap))
     {'apps': {'ipython': {'command': 'snap/command-chain/snapcraft-runner '
                                      '$SNAP/command-ipython.wrapper',
                           'plugs': ['home', 'network', 'network-bind']},
               'python': {'command': 'snap/command-chain/snapcraft-runner '
                                     '$SNAP/command-python.wrapper',
                          'plugs': ['home', 'network', 'network-bind']},
               'snap-helpers': {'command': 'snap/command-chain/snapcraft-runner '
                                           '$SNAP/command-snap-helpers.wrapper',
                                'plugs': ['home', 'network', 'network-bind']}},
      'architectures': ['amd64'],
      'base': 'core18',
      'confinement': 'strict',
      'description': 'Test snap for snap-helpers.\n'
                     '\n'
                     'It provides python and ipython shells to test the '
                     '`snaphelpers` library.\n',
      'grade': 'stable',
      'name': 'snap-helpers',
      'summary': 'Test snap for snap-helpers',
      'version': '0.1.6+git6.37370cd'}


Hook helpers
------------

The library provides helpers to reduce boilerplate when setting up hooks for the snap.

Hooks can be defined by simply registering functions to be called as hooks via
``entry_points`` in the application ``setup.py``:

.. code:: python

   setup(
       # ...
       entry_points={
           "snaphelpers.hooks": [
               "configure = testapp:configure_hook",
               "install = testapp:install_hook",
           ]
       }
   )

Hook functions are called with a ``Snap`` object as argument:

.. code:: python

   def install_hook(snap: snaphelpers.Snap):
       # ...


   def configure_hook(snap: snaphelpers.Snap):
       # ...

``snap-helpers`` will take care of the hooks plumbing (i.e. creating hook files
in ``$SNAP/snap/hooks``).

Alternatively, the configuration can be done in ``setup.cfg``:

.. code:: ini

   [options.entry_points]
   snaphelpers.hooks =
       install = testapp:install_hook
       configure = testapp:configure_hook


Testing with the snap
---------------------

The ``snap-helpers`` snap provides a way to easily test code using the library in
a real snap environment with strict confinement.

It provides an IPython_ shell which automatically imports the ``snaphelpers``
module and provides a ``Snap`` instance for the current snap.

.. code::

   $ snap-helpers
   Python 3.6.8 (default, Aug 20 2019, 17:12:48)
   Type 'copyright', 'credits' or 'license' for more information
   IPython 7.8.0 -- An enhanced Interactive Python. Type '?' for help.


   Use the "snap" variable for an instance for the current snap.

   In [1]: import pprint

   In [2]: pprint.pprint(dict(snap.environ))
   {'ARCH': 'amd64',
    'COMMON': '/var/snap/snap-helpers/common',
    'CONTEXT': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890',
    'COOKIE': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890',
    'DATA': '/var/snap/snap-helpers/x1',
    'INSTANCE_KEY': '',
    'INSTANCE_NAME': 'snap-helpers',
    'LIBRARY_PATH': '/var/lib/snapd/lib/gl:/var/lib/snapd/lib/gl32:/var/lib/snapd/void',
    'NAME': 'snap-helpers',
    'REEXEC': '',
    'REVISION': 'x1',
    'SNAP': '/snap/snap-helpers/x1',
    'USER_COMMON': '/home/ack/snap/snap-helpers/common',
    'USER_DATA': '/home/ack/snap/snap-helpers/x1',
    'VERSION': '0.1.6+git1.4a0b997'}

The snap can be built and installed as follows:

.. code:: shell

   $ snapcraft
   $ sudo snap install --dangerous snap-helpers_*.snap


Installation
------------

``snap-helpers`` can be installed from PyPI_.

Run:

.. code:: shell

   $ pip install snap-helpers


Documentation
-------------

Full documentation is available on ReadTheDocs_.


.. _IPython: https://ipython.org/
.. _PyPI: https://pypi.org/
.. _ReadTheDocs: https://snap-helpers.readthedocs.io/en/latest/

.. |Latest Version| image:: https://img.shields.io/pypi/v/snap-helpers.svg
   :alt: Latest Version
   :target: https://pypi.python.org/pypi/snap-helpers
.. |Build Status| image:: https://github.com/albertodonato/snap-helpers/workflows/CI/badge.svg
   :alt: Build Status
   :target: https://github.com/albertodonato/snap-helpers/actions?query=workflow%3ACI
.. |Coverage Status| image:: https://img.shields.io/codecov/c/github/albertodonato/snap-helpers/main.svg
   :alt: Coverage Status
   :target: https://codecov.io/gh/albertodonato/snap-helpers
.. |Documentation| image:: https://readthedocs.org/projects/snap-helpers/badge/?version=stable
   :alt: Documentation
   :target: https://snap-helpers.readthedocs.io/en/stable/?badge=stable
