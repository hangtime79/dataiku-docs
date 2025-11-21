Load balancers
##############

Fleet Manager manages load balancers.

They act as application gateways in front of Dataiku nodes. They can also be used to perform load balancing in front of automation nodes to achieve high availability.

Dashboard
=========

The main screen through which you will get information about the load balancer is the dashboard. It is refreshed automatically and displays the different node mappings, the components created in the cloud and status information.

Lifecycle
=========

Provisioning
------------

The provisioning is a sequence of operations required to have the load balancer created in the cloud.

Updating
--------

When modifying the load balancer configuration in Fleet Manager, the load balancer must be updated for the changes to be propagated to the cloud. A reconciliation mechanism automatically detects these modifications and updates the relevant cloud structures to align with the defined configuration.

Deprovisioning
--------------

Deprovisioning a load balancer consists of deleting the different cloud objects that were created as well as the load balancer.

Settings
========

A load balancer has various settings.

.. note::
    You can create a load balancer at fleet creation time using the **Fleet blueprints**.

    In this case, a best practice setup will be implemented:
    * No public IP for the DSS nodes
    * The load balancer exposes the DSS nodes
    * The load balancer forwards traffic to the DSS nodes with HTTP

Virtual network
---------------

Select the virtual network in which the load balancer will be created. This virtual network needs to have two subnets defined in Fleet Manager. Note that the secondary subnet can be added at any time but won't be editable afterwards.

Virtual network HTTPS strategy
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The virtual network **HTTPS strategy** only applies to the nodes. The load balancer can still be exposed using HTTPs.

.. note::
    If your virtual network HTTPS strategy is **Self-signed certificates**, you need to add manually the self-signed certificate to the load balancer.

Node mappings
-------------

Node mappings define the hostnames that point to each DSS node.

Each node must have a unique hostname, except for automation nodes which can share the same hostname for load balancing purposes.

.. note::
    If the virtual network DNS strategy is **Assign a Route53 domain name you manage**, the hostnames correspond to sub domains within this zone. Fleet Manager will manage both the sub domains and the load balancer.

    Otherwise, the hostnames must be fully qualified domain names.

Certificate mode
----------------

Assigns a certificate to the load balancer to secure the load balancer hostnames.

Multiple modes are available:

- **No certificate**
- **Certificate ARN**: Certificate has been created in AWS console and its ARN is used to assign it to the load balancer
- **Certificate manager**: A certificate will be created by Fleet Manager in the provided certificate manager. This works only if the DNS is also managed by Fleet Manager through the virtual network (see :ref:`virtual networks DNS strategy <aws-cloudstacks-vnet-dnsstrategy>`). It ensures that Fleet Manager fully manages the certificate: if the hostnames are modified, the certificate will be automatically regenerated accordingly

Public IP mode
--------------

Assigns a public IP to the load balancer.

Only **Dynamic public IP** mode is supported. Fleet Manager will manage the load balancer public IP.
