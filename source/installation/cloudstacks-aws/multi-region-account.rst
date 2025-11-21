Multi-region and multi-account support
######################################

Fleet Manager can manage cloud objects across different regions and impersonate different identities.

By default, it operates within the same region where it is deployed and uses its own identity.

If you are reusing an existing Fleet Manager role, ensure that its permissions match those documented in the :doc:`Fleet Manager installation procedure </installation/cloudstacks-aws/guided-setup-new-vpc-elastic-compute>`.

Multi-account support
=====================

In order to manipulate cloud objects with a different identity, an account needs to be created in Fleet Manager.

This account needs the same permissions as the :doc:`initial Fleet Manager account</installation/cloudstacks-aws/guided-setup-new-vpc-elastic-compute>`.

Multiple authentication modes are available:

- **IAM role**
- **Keypair**

IAM role
--------

When using another IAM role, Fleet Manager role needs to be added to its *Trust Relationship*.

Multi-region support
====================

To enable multi-region functionality, you need to create a new VPC in the AWS console, following the same process used when setting up the Fleet Manager VPC during the :doc:`Fleet Manager installation </installation/cloudstacks-aws/guided-setup-new-vpc-elastic-compute>`. Ensure that its IP range does not overlap with the Fleet Manager VPC's IP range.

When creating the corresponding virtual network in Fleet Manager, specify the desired region. Any objects deployed in this virtual network will be located in that region.

In this case, both the virtual network where Fleet Manager is deployed and the virtual network where the objects will be deployed must be paired. Fleet Manager can handle this pairing process.

Combining Multi-region and Multi-account
========================================

You can use both multi-region and multi-account capabilities simultaneously.

To do so, select an account different from the default Fleet Manager account when creating a virtual network in Fleet Manager.
