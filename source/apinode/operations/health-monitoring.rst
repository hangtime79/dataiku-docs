Health monitoring
##################

.. contents::
	:local:

Global isAlive probe
=====================

The API node features a global "isAlive" probe that can be used by a load balancer to query the status of the server.

The global isAlive probe does not actually perform validation that the individual services on the API node are properly running.

isAlive API
------------

The isAlive probe is available on the ``/isAlive/`` HTTP mount point. This URI returns:

* An HTTP success code (2xx) if the probe considers the node as alive
* An HTTP server error code (5xx) if the probe considers the node as not alive

Forcing the node as not alive
-------------------------------

You can force the isAlive probe to indicate that the node is not alive, without actually interrupting the traffic. This will lead the load balancer to redirect the traffic to other nodes, and is generally used for rolling upgrades scenarii.

To force the node as not alive:

* Create a file called ``apinode-not-alive.txt`` in the API node data directory

To get back to normal:

* Remove the file ``apinode-not-alive.txt`` from the API node data directory



Monitoring the status of services
===================================

To monitor the precise status of service, we recommend that you perform a regular prediction query, which will actually exercice the whole chain.