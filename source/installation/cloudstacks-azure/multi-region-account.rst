Multi-region and multi-account support
######################################

Fleet Manager can manage cloud objects across different regions and impersonate different identities.

By default, it operates within the same region where it is deployed and uses its own identity.

If you are reusing an existing Fleet Manager role, ensure that its permissions match those documented in the :doc:`Fleet Manager installation procedure </installation/cloudstacks-azure/guided-setup-new-vnet-elastic-compute>`.

Multi-account support
=====================

In order to manipulate cloud objects with a different identity, an account needs to be created in Fleet Manager.

This account needs the same permissions as the :doc:`initial Fleet Manager account</installation/cloudstacks-azure/guided-setup-new-vnet-elastic-compute>`.

The following information need to be specified:

- **Environment**
- **Subscription**
- **Tenant ID**

Multiple authentication modes are available:

- **Managed identity**: The resource ID of the managed identity has to be provided
- **Application with secret credentials**: The application (client) ID has to be provided
- **Application with certificate credentials**: The application (client) ID has to be provided

Multi-region support
====================

In the region where you want to manage the cloud objects:

- Create a new resource group
- Create a new network security group and add an inbound rule *IngressAllowForFM* with the following configuration:

    - Source: ``IP Adresses``
    - CIDR range: ``0.0.0.0/0``
    - Destination: ``Service Tag``
    - Destination service tag: ``VirtualNetwork``
    - Service: ``Custom``
    - Destination port ranges: ``22,80,443``
    - Protocol: ``TCP``

- Create a new virtual Network with an IP range that does not conflict with the one in Fleet Manager virtual Network
- Add a role Assignment to your virtual network for Fleet Manager managed identity as a *Network contributor*
- Create a subnet in this virtual Network using the previously created network security group
- Add a role Assignment to your resource group for Fleet Manager managed identity as a *Contributor*

When creating the corresponding virtual network in Fleet Manager, specify the desired region. Any objects deployed in this virtual network will be located in that region.

In this case, both the virtual network where Fleet Manager is deployed and the virtual network where the objects will be deployed must be paired. Fleet Manager can handle this pairing process.

Combining Multi-region and Multi-account
========================================

You can use both multi-region and multi-account capabilities simultaneously.

To do so, select an account different from the default Fleet Manager account when creating a virtual network in Fleet Manager.
