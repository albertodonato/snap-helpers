Managing snap services
======================

Snaps can define commands to be run as services (via systemd).

The list of services defined in the snap, along with their status, is
accessible via :class:`.SnapServices.list()`.This returns a dict with
:class:`.SnapService` instances by service name.

The :class:`.SnapService` class allows interacting with a specific service:

.. code:: python

   >>> from snaphelpers import SnapServices
   >>> services = SnapServices()
   >>> services.list()
   {'service1': <snaphelpers._service.SnapService object at 0x7fa4da982cc0>, 'service2': <snaphelpers._service.SnapService object at 0x7fa4da982c50>}
   >>> service1 = services.list()['service1']
   >>> service1.name
   'service1'
   >>> service1.enabled, service1.active
   (True, False)
   >>> service1.notes
   []
   >>> service1.start()
   >>> service1.enabled, service1.active
   (True, True)
   >>> service1.stop(disable=True)
   >>> service1.enabled, service1.active
   (False, False)


It's also possible to start/stop/restart all services from the :class:`.SnapServices` instance:

.. code:: python

   >>> services.start(enable=True)
   >>> [(s.name, s.active, s.enabled) for s in services.list().values()]
   [('service1', True, True), ('service2', True, True)]
   >>> services.stop(disable=True)
   >>> [(s.name, s.active, s.enabled) for s in services.list().values()]
   [('service1', False, False), ('service2', False, False)]
