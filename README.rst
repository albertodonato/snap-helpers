snap-helpers - Interact with the Snap system within a Snap
==========================================================

|Latest Version| |Snap Package| |Build Status| |Coverage Status| |Documentation|


A Python library to interact with snap configuration and properties from inside a snap.

It exposes a top-level ``snaphelpers.Snap`` object which provides access to:

- snap details:

  .. code:: python

     >>> snap = snaphelpers.Snap()
     >>> snap.name
     'snap-helpers'
     >>> snap.instance_name
     'snap-helpers'
     >>> snap.version
     '0.3.0+git5.5794660'
     >>> snap.revision
     '138'

- paths:

  .. code:: python

     >>> snap.paths.common
     PosixPath('/var/snap/snap-helpers/common')
     >>> snap.paths.data
     PosixPath('/var/snap/snap-helpers/138')
     >>> snap.paths.real_home
     PosixPath('/home/ack')
     >>> snap.paths.snap
     PosixPath('/snap/snap-helpers/138')
     >>> snap.paths.user_common
     PosixPath('/home/ack/snap/snap-helpers/common')
     >>> snap.paths.user_data
     PosixPath('/home/ack/snap/snap-helpers/138')

- snap-related environment variables:

  .. code:: python

     >>> pprint.pprint(dict(snap.environ))
     {'ARCH': 'amd64',
      'COMMON': '/var/snap/snap-helpers/common',
      'CONTEXT': 'XbhAD8QBMDwJiEi5LcN-5fCrVeAG7qBGojWiWA0vXkx0hX-JxyqX',
      'COOKIE': 'XbhAD8QBMDwJiEi5LcN-5fCrVeAG7qBGojWiWA0vXkx0hX-JxyqX',
      'DATA': '/var/snap/snap-helpers/138',
      'INSTANCE_KEY': '',
      'INSTANCE_NAME': 'snap-helpers',
      'LIBRARY_PATH': '/var/lib/snapd/lib/gl:/var/lib/snapd/lib/gl32:/var/lib/snapd/void',
      'NAME': 'snap-helpers',
      'REAL_HOME': '/home/ack',
      'REEXEC': '',
      'REVISION': '138',
      'SNAP': '/snap/snap-helpers/138',
      'USER_COMMON': '/home/ack/snap/snap-helpers/common',
      'USER_DATA': '/home/ack/snap/snap-helpers/138',
      'VERSION': '0.3.0+git5.5794660'}
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
     SnapMetadataFile(/snap/snap-helpers/138/meta/snap.yaml)
     >>> pprint.pprint(dict(snap.metadata_files.snap))
     {'apps': {'python': {'command': 'bin/python3',
                          'plugs': ['home', 'network', 'network-bind']},
               'snap-helpers': {'command': 'bin/snap-helpers-shell',
                                'plugs': ['home', 'network', 'network-bind']}},
      'architectures': ['amd64'],
      'base': 'core22',
      'confinement': 'strict',
      'description': 'Test snap for the snap-helpers Python library.\n'
                     '\n'
                     'It provides python and ipython shells to interact and test '
                     'the `snaphelpers`\n'
                     'library.\n'
                     '\n'
                     'See the https://github.com/albertodonato/snap-helpers for '
                     'more details.\n',
      'environment': {'LD_LIBRARY_PATH': '${SNAP_LIBRARY_PATH}${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}:$SNAP/lib',
                      'PATH': '$SNAP/usr/sbin:$SNAP/usr/bin:$SNAP/sbin:$SNAP/bin:$PATH'},
      'grade': 'stable',
      'license': 'LGPL-3.0',
      'name': 'snap-helpers',
      'slots': {'snap-helpers-lib': {'content': 'snap-helpers-lib',
                                     'interface': 'content',
                                     'read': ['$SNAP/lib/python3.10/site-packages/snaphelpers']}},
      'summary': 'Test snap for the snap-helpers Python library.',
      'version': '0.3.0+git5.5794660'}


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

or in ``setup.cfg`` with:

.. code:: ini

   [options.entry_points]
   snaphelpers.hooks =
       install = testapp:install_hook
       configure = testapp:configure_hook


Hook functions are called with a ``Snap`` object as argument:

.. code:: python

   def install_hook(snap: snaphelpers.Snap):
       # ...


   def configure_hook(snap: snaphelpers.Snap):
       # ...

``snap-helpers`` will take care of the hooks plumbing (i.e. creating hook files
in ``$SNAP/snap/hooks``).



Testing with the snap
---------------------

The ``snap-helpers`` snap provides a way to easily test code using the library in
a real snap environment with strict confinement.

It provides an IPython_ shell which automatically imports the ``snaphelpers``
module and provides a ``Snap`` instance for the current snap.

.. code::

   $ snap-helpers
   Python 3.10.4 (main, Jun 29 2022, 12:14:53) [GCC 11.2.0]
   Type 'copyright', 'credits' or 'license' for more information
   IPython 8.7.0 -- An enhanced Interactive Python. Type '?' for help.


   Use the "snap" variable for an instance for the current snap.

   In [1]: import pprint

   In [2]: pprint.pprint(dict(snap.environ))
   {'ARCH': 'amd64',
    'COMMON': '/var/snap/snap-helpers/common',
    'CONTEXT': 'XbhAD8QBMDwJiEi5LcN-5fCrVeAG7qBGojWiWA0vXkx0hX-JxyqX',
    'COOKIE': 'XbhAD8QBMDwJiEi5LcN-5fCrVeAG7qBGojWiWA0vXkx0hX-JxyqX',
    'DATA': '/var/snap/snap-helpers/138',
    'INSTANCE_KEY': '',
    'INSTANCE_NAME': 'snap-helpers',
    'LIBRARY_PATH': '/var/lib/snapd/lib/gl:/var/lib/snapd/lib/gl32:/var/lib/snapd/void',
    'NAME': 'snap-helpers',
    'REAL_HOME': '/home/ack',
    'REEXEC': '',
    'REVISION': '138',
    'SNAP': '/snap/snap-helpers/138',
    'USER_COMMON': '/home/ack/snap/snap-helpers/common',
    'USER_DATA': '/home/ack/snap/snap-helpers/138',
    'VERSION': '0.3.0+git5.5794660'}

The snap can be built and installed as follows:

.. code:: shell

   $ snapcraft -v
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
.. |Snap Package| image:: https://snapcraft.io/snap-helpers/badge.svg
   :alt: Snap Package
   :target: https://snapcraft.io/snap-helpers
.. |Build Status| image:: https://github.com/albertodonato/snap-helpers/workflows/CI/badge.svg
   :alt: Build Status
   :target: https://github.com/albertodonato/snap-helpers/actions?query=workflow%3ACI
.. |Coverage Status| image:: https://img.shields.io/codecov/c/github/albertodonato/snap-helpers/main.svg
   :alt: Coverage Status
   :target: https://codecov.io/gh/albertodonato/snap-helpers
.. |Documentation| image:: https://readthedocs.org/projects/snap-helpers/badge/?version=stable
   :alt: Documentation
   :target: https://snap-helpers.readthedocs.io/en/stable/?badge=stable
