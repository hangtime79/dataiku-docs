High availability and scalability
###################################

.. contents::
	:local:

DSS API node is natively highly available and scalable. Both high availability and scalability are achieved by deploying multiple instances of the API node.

Each DSS API Node instance is fully independent. A client of the API can query any API node instance.

It is recommended that you read how services are created and deployed first: :doc:`/apinode/introduction`

HA deployment
==============

A standard deployment of high availability for API node includes:

* Deploying several instances of the API node software on separate machines
* Transfering new packages on all API node servers
* Activating new versions of the packages on all API node servers

* Using a client-side high availability mechanism

Two main mechanisms exist for client-side HA handling:

* Using a load balancer
* Using client-side dispatch / retry / fallback

Load balancer
--------------

With a load balancer (either hardware, like F5, software like HAProxy, or cloud like AWS ELB), you add a layer in front of all your API node instances. The load balancer (which is itself highly available) receives the queries, dispatches them to all API node instances that are currently available.

The load balancer continuously monitors the API node instances to know which ones are healthy and which ones are not. To know more about the monitoring probe built-in in the API node, see :doc:`health-monitoring`.

You'll need to refer to the documentation of your load balancer to know how to configure it to provide high availability for API node.

Client-side dispatch
---------------------

The load balancer solution has the main advantage that it is transparent from the clients. The client simply queries the load balancer URL and automatically gets a highly available and scalable service.

There are drawbacks, though. A truly HA load balancer solution is fairly costly and complex to deploy.

Since API node queries are "side-effect-free", it is also possible to have the client perform the dispatching, and retry of queries. This makes for a slightly more complex client code. Furthermore, the client needs to know all URLs of all API node instances, which can make it more cumbersome to deploy additional API node instances (to provide for an increase in traffic).


Zero-downtime generation update
================================

Activating a new generation of a service on an API node does not create any loss of queries. Existing queries will continue being served using the old generation, and all new queries go to the new generation, as soon as it is ready.


Handling software updates
==========================

The API node software allows you to perform software updates without losing queries.

.. note::

	Deploying new major or minor versions of the API node software generally requires creating a new version of the package first, as the on-disk format of packages may change.

A rolling software update involves executing the following steps on each API node software, in turn:

* Taking the node out of the high availability, generally by forcing the isAlive probe to return false (See :doc:`health-monitoring`)
* Stopping the node
* Upgrading the node
* Restarting the node
* Uploading the new version of the package on the node
* Getting the node back into the high availability pool
