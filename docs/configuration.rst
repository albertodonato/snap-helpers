Managing snap configuration
===========================

Snap configuration is managed through :class:`.SnapConfig` (which is also
accessible as :attr:`config` in the :class:`.Snap` object).

To get configuration for a set of keys, :meth:`.SnapConfig.get_options` can be
used. This returns a :class:`.SnapConfigOptions` instance, which allows
accessing subkeys of the specified top-level keys with a dict-like interface.

It's possible to use dotted-notation to access subkeys.

.. code:: python

   >>> from snaphelpers import SnapConfig
   >>> config = SnapConfig()
   >>> options = config.get_options('foo', 'asdf')
   >>> options['foo']
   {'bar': 'baz'}
   >>> options['foo.bar']
   'baz'
   >>> options['asdf']
   3
   >>> options.as_dict()
   {'asdf': 3, 'foo': {'bar': 'baz'}}


It's also possible to get a single value for a key (at any level) with
:meth:`.SnapConfig.get`:
     
.. code:: python

   >>> config.get('foo.bar')
   'baz'


Configuration options can be set in bulk by passing a dict with keys and
values. Values can be of any JSON-serializable type, and keys can use the
dotted-notation to only set certain subkeys:

.. code:: python

   >>> config.set({'foo.bar': 'baz', 'asdf': 3})

.. note:: calling :meth:`.SnapConfig.set` requires root access.
