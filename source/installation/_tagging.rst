.. |rArr|   unicode:: U+021D2 .. RIGHTWARDS DOUBLE ARROW

Tagging on Dataiku Cloud Stacks
###############################

Dataiku Cloud Stacks (DCS) allows to tag (or label) cloud resources in order to leverage cloud provider specific features such as managing, identifying, organizing, searching for, and filtering resources.
Cloud tags are supported on the following DCS entities:

* Tenants
* Cloud Accounts
* Virtual Networks
* Load Balancers
* Instances

Cloud tags are key-value pairs that are applied as metadata on the cloud resources created by DCS during provisioning of entities like instances or load balancers.
Some entities like cloud accounts are not provisioned and do not create cloud resources themselves, but tags are inherited according to the following hierarchy:

.. centered::
    Tenants |rArr| Cloud Accounts |rArr| Virtual Networks |rArr| Load Balancers |rArr| Instances

This means that any cloud tags in a Tenant will be inherited by the Cloud Accounts in that Tenant, that any cloud tags in a Cloud Account will be inherited by the Virtual Networks attached to that Cloud Account, etc.

You will be able to find a list of inherited tags in the Virtual Networks, Load Balancers and Instances dashboard pages:

.. image:: /installation/img/virtual-network-withaccount-dashboard-tags.png
   :alt: Display of the cloud tags and inherited tags on the dashboard of a Virtual Network attached to a Cloud Account.

Cloud tags are also now displayed on the listing pages of Instances, Load Balancers, Cloud Accounts and Virtual Networks.
They can also be used for filtering the list.

.. image:: /installation/img/instances-list-tags.png
   :alt: List of instances contains the cloud tags.

Limitations
===========

Tagging in Dataiku Cloud Stacks has some limitations related to the cloud provider that the platform is deployed on. Please refer to each Cloud specific requirements section for more information.

Tags are not updated on cloud resources while saving of the form of the entity being modified. The entity must be reprovisioned for the new tags to be applied when supported.

Virtual Networks are not reprovisionable, thus the resources created (e.g. security groups) will not be updated with new tags upon modification.
However, due to the inheritance, new or reprovisioned instances and load balancers created within the Virtual Network will contain the updated tags.

.. warning::
    The data disk of an instance is kept throughout its lifecycle, thus reprovisioning will overwrite already existing tags and add new ones, but it will not delete ones that were removed.
    Be mindful that tags may accumulate on the data disk of an instance if changed often and this might cause issues related to Cloud provider limitations.
