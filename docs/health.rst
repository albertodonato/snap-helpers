Snap health
===========

Since version 2.41, ``snapd`` supports `health status checks`_ for snaps via the ``check-health`` hook.

When implementing hooks with ``snap-helpers``, it's possible to set the health
status for the snap via :class:`.SnapHealth`.

This provides methods for each of the supported health statuses:

  .. code:: python

     >>> snap.health.okay()
     >>> snap.health.waiting('foo must happen first', code='wait-foo')
     >>> snap.health.blocked('nothing to do for now')
     >>> snap.health.error('something is wrong', code='bar-wrong')

Note that for any status other than ``okay``, a message is required. Error code
is optional.


.. _`health status checks`: https://forum.snapcraft.io/t/health-checks/10605
