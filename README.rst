snap-helpers - Interact with the Snap system within a Snap
==========================================================

|Build Status| |Coverage Status|

..
   |Latest Version| |Build Status| |Coverage Status| |Documentation Status|


   Installation
   ------------

   snap-helpers can be installed from PyPI_.

   As a user run::

     $ pip install snap-helpers

   Documentation
   -------------

   Full documentation is available on ReadTheDocs_.


Testing with the snap
---------------------

The `snap-helpers` snap provides a way to easily test code using the library in
a real snap environment with strict confinement.

It provides the `python` and `ipython` commands:

.. code::

   $ snap-helpers.python -c 'from pprint import pprint; import snaphelpers; pprint(dict(snaphelpers.SnapEnviron()))'
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
    'VERSION': '0+git.26e1e9d'}

The snap can be built and installed as follows:

.. code:: shell

   $ snapcraft
   $ sudo snap install --dangerous snap-helpers_*.snap


.. _ReadTheDocs: https://snap-helpers.readthedocs.io/en/latest/
.. _PyPI: https://pypi.python.org/

.. |Latest Version| image:: https://img.shields.io/pypi/v/snap-helpers.svg
   :target: https://pypi.python.org/pypi/snap-helpers
.. |Build Status| image:: https://img.shields.io/travis/albertodonato/snap-helpers.svg
   :target: https://travis-ci.com/albertodonato/snap-helpers
.. |Coverage Status| image:: https://img.shields.io/codecov/c/github/albertodonato/snap-helpers/master.svg
   :target: https://codecov.io/gh/albertodonato/snap-helpers
.. |Documentation Status| image:: https://readthedocs.org/projects/snap-helpers/badge/?version=stable
   :target: https://snap-helpers.readthedocs.io/en/stable/?badge=stable
