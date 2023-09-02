===========================
Device to Endpoint dataflow
===========================

In order for RadLoggerPy to be effective, measured data from devices needs to
be passed to the necessary endpoints such that they can be stored, processed or
transferred.

.. _`Include any references` : https://docs.openstack.org/oslo.config/latest/

Problem Description
*******************

The interfaces and dataflow between the devices and endpoints needs to be
carefully designed such that it is maintainable, flexible, easy to extend and
performant.

Use Cases
*********

- Users, want their device measurement data to be stored and processed such that
  they can access it later.

Proposed Change
***************

Devices gain access to a (bounded) lockless queue to which they can submit
the measurements.

Endpoint data is delivered by a publish / subscribe message brokers that pulls
data from this lockless queue.

When data is delivered to an endpoint it is awoken using a condition.

The effectiveness of this and slightly different solutions should be evaluated
in unit tests.

..
    dataflow-uml.drawio

.. image:: /images/dataflow-uml.svg
    :align: center
    :width: 100%
    :alt: Dataflow UML diagram between devices and endpoints

Alternatives
------------

Instead of endpoints each running in dedicated threads, the task of processing
data should be submitted to a threadpool.

Work Items
------------

- Develop test framework to evaluate end to end dataflow performance between
  solutions.
- Implement lockless queue for device data.
- Implement publish / subscribe message broker and decide on topics scheme.
- Implement endpoint interface.
- Implement most basic endpoint (logging).

Database model impact
*********************

None

Dependencies
************

- A lockless thread-safe queue for Python
- A publish / subscribe framework for Python

References
**********

1. `atomic-queue`_
2. `pypubsub`_
3. `pydispatcher`_

.. _atomic-queue: https://pypi.org/project/atomic-queue/
.. _pypubsub: https://pypi.org/project/PyPubSub/
.. _pydispatcher: https://pydispatcher.sourceforge.net/

History
*******

.. list-table:: Revisions
   :header-rows: 1

   * - Release Name
     - Description
   * - v0.5.0
     - Introduced