Multi-region and multi-account support
######################################

Fleet Manager can manage cloud objects across different regions and impersonate different identities.

By default, it operates within the same region where it is deployed and uses its own identity.

If you are reusing an existing Fleet Manager role, ensure that its permissions match those documented in the :doc:`Fleet Manager installation procedure </installation/cloudstacks-gcp/guided-setup-new-vpc-elastic-compute>`.

Multi-account support
=====================

In order to manipulate cloud objects with a different identity, an account needs to be created in Fleet Manager.

One authentication mode is available:

- **JSON key**

JSON key
--------

- Create a service account the same way Fleet Manager service account was created during :doc:`Fleet Manager installation </installation/cloudstacks-gcp/guided-setup-new-vpc-elastic-compute>`
- Create a JSON key for this service account and take note of the key JSON content

Multi-region support
====================

In Google Cloud Console, a new VPC in the target region has to be created the same way Fleet Manager VPC was created in :doc:`Fleet Manager installation </installation/cloudstacks-gcp/guided-setup-new-vpc-elastic-compute>`.

When creating the corresponding virtual network in Fleet Manager, specify the desired region. Any objects deployed in this virtual network will be located in that region.

In this case, both the virtual network where Fleet Manager is deployed and the virtual network where the objects will be deployed must be paired. Fleet Manager can handle this pairing process.

Make sure the *Compute Engine API* is activated on your project as it will be required when creating the VPC.

Combining Multi-region and Multi-account
========================================

You can use both multi-region and multi-account capabilities simultaneously.

To do so, select an account different from the default Fleet Manager account when creating a virtual network in Fleet Manager.
