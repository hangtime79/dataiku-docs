Conceptual overview
####################

Fleet Manager (FM)
==================

The Dataiku Cloud Stacks for AWS setup uses a central component, called Dataiku Fleet Manager (FM) in order to deploy, upgrade, backup, restore and configure one or several Dataiku instances.

Fleet Manager handles the entire lifecycle of the Dataiku instances, freeing you from most administration tasks. The instances managed by Fleet Manager come builtin with the ability to scale computation on elastic computation clusters, powered by Kubernetes.

To deploy Dataiku Cloud Stacks for AWS, Dataiku provides a Cloud Formation template that deploys Fleet Manager. From Fleet Manager, you then deploy the Dataiku instances.

Instance
========

An instance is a single installation of a DSS design node, automation node or deployer node. It is the main object manipulated by FM. Each instance is backed by a virtual machine dedicated to it.

When you create an instance, you *provision* it. Provisioning an instance means FM creates the required cloud resources to host the DSS node. See :ref:`instances lifecycle <cloudstacks-instance-lifecycle>` for more information.


Instance template
=================

An instance template is a set of configuration information that can be reused to start several instances with common properties. An instance is always launched from an instance template and stays linked to it throughout its lifetime.

Modifying an instance template impacts the provisioning behavior of all the instances launched from it. Reprovisioning is not enforced, but required for the new setup to be applied.

Virtual network
===============

A virtual network represents the network context in which the instances will be launched. That means a reference to the virtual network used in the cloud provider, but also other configurations such as how DNS and HTTPS are handled.

Instance templates are not tied to a specific virtual network.

Load balancer
=============

A load balancer is a device that distributes traffic across different instances.

It acts as an application gateway by linking hostnames to various instances and helps secure inbound traffic.

For automation nodes, it can also perform actual load balancing to ensure high availability.

Account
=======

An account represents an identity manipulating the objects in the cloud on behalf of Fleet Manager.

.. _cloudstacks-concept-agent:

Agent
=====

The FM agent is a Dataiku software that runs alongside DSS in your instances. It manages communication with the FM server, sends technical information to it, and performs administrative tasks on behalf of the FM server authority.
