Managing snap configuration
===========================

Snap configuration is managed through :class:`.SnapConfig` (which is also
accessible as :attr:`config` in the :class:`.Snap` object).

  .. code:: python

     >>> from snaphelpers import SnapConfig
     >>> config = SnapConfig()
     >>> config.set({'foo.bar': 'baz', 'asdf': 3})
     >>> options = config.get_options('foo', 'asdf')
     >>> options['foo']
     {'bar': 'baz'}
     >>> options['foo.bar']
     'baz'
     >>> options['asdf']
     3
     >>> options.as_dict()
     {'asdf': 3, 'foo': {'bar': 'baz'}}
     >>> config.get('foo.bar')
     'baz'


The :meth:`.SnapConfig.get_options` returns a :class:`.SnapConfigOptions`
instance which wraps configuration for the specified top-level keys.

Values are accessible in a dict-like form which allows dotted notation for keys.

.. note:: calling :meth:`.SnapConfig.set` requires root access.
