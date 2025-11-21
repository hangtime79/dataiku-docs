Virtual networks
################

A virtual network in Fleet Manager is an object representing the networking setup of instances created into it.

The virtual network defines in which VPC and subnet the instances will be launched, as well as how DNS hostnames and HTTPS certificates for the instances will be used.

Each instance belongs to a virtual network. At least one virtual network is required to deploy instances.

Networking requirements
=======================

The most important requirement is that the DSS instances must be able to reach FM on its main port. FM has a single URL that must be reachable by all DSS instances it creates, even if they span over several networks.

Creation
========

Go to *Virtual networks* and click on *New virtual network* at the top right. You will be required to provide the mandatory values for virtual networks:

* *Label*: the name of the network that will be displayed in FM. It can be changed later.
* *VPC id*: Id of the VPC in which you want to deploy instances. If is pre-filled with the VPC in which FM is currently running. It cannot be changed after creation.
* *Subnet id*: Id of the subnet in which you want to deploy instances. If is pre-filled with the subnet in which FM is currently running. It cannot be changed after creation.
* *Security groups*: By default, FM automatically creates security groups when creating the virtual network. You can also manually list security groups you want attached on the created instances.


.. note:: Auto-creation of security groups adds two groups:

   - A security group that opens SSH (22), HTTP (80) and HTTPS (443) on all traffic.
   - A "default"-like security group that allows all traffic between instances having it attached. It is used for elastic AI setups where clusters need to be able to contact back the instances.

Edition
=======

Once a virtual network has been created, you can edit its settings.

Public IP address
-----------------

By default, FM assigns public IPs to your instances. You can disable this. Note that this requires that the subnet on which the instances are
started has a default route through an Internet Gateway

Changing the public IP policy requires reprovisioning the affected instances.

.. _aws-cloudstacks-vnet-dnsstrategy:

DNS Strategy
------------

By default, instances only get IP addresses. FM can assist in assigning hostnames. It is also required if you want to apply a verified HTTPS strategy.

Changing the DNS strategy requires reprovisioning the affected instances.

In the virtual networks list, click on the desired network to display its dashboard, then select the *Settings* tabs to change the configuration. Select *Assign a Route53 domain name* in the *DNS Strategy*  drop-down menu. Then fill in the Zone ID for each required zone, one to have DNS records for private IPs, a second one for the public IPs. If you need only one, let the unused field empty. Click on *Save* at the top right to apply your changes.

If using DNS records for both private IPs and public IPs, the zone IDs must be distinct.

The IAM Role used by the Fleet Manager must have the following permissions:

   .. code-block:: text

     route53:GetHostedZone
     route53:ChangeResourceRecordSets


HTTPS configuration
-------------------

By default, instances are deployed with self-signed certificates. These will trigger security alerts in your browser.

FM supports several strategies for configuring HTTPS.

None
%%%%

This simple mode means no certificate is involved and instances are exposed on HTTP.

Self-signed certificate
%%%%%%%%%%%%%%%%%%%%%%%

This is the default. When using this strategy, each instance will create its own self-signed certificate if none exists yet, and uses it to expose DSS on port 443. You can choose wether HTTP is closed or redirects to HTTPS.

Additional domain names can be handled by the self-signed certificate at instance level.

Custom certificate for each instance
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Select *Enter a certificate/key for each instance* to use the certificates emitted with by your PKI. When using this strategy,
each instance will have to be configured with the certificate and private key intended for it.
The secret key can be stored encrypted by FM or into your cloud provider secret manager.

You can choose wether HTTP is closed or redirects to HTTPS.

This mode requires instance level settings.

Let's Encrypt
'''''''''''''

This mode makes use of `Let's Encrypt <https://letsencrypt.org/>`_ and `certbot <https://certbot.eff.org/>`_ to generate and renew automatically a publicly recognized certificate.
When using this mode, you must specify an email address representing the legal person owning the certificate.

Instances must be reachable on HTTP (80) and HTTPS (443) from the internet.

Additional domain names can be added at instance level.

.. warning:: Let's Encrypt service has `rate limits <https://letsencrypt.org/docs/rate-limits/>`_ that makes it unsuitable
   for numerous deletions and creations. Be careful to use it for stable deployments. If you hit your quota, there is no way
   to reset it.
