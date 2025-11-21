Global settings
################

There are only a few global settings in Fleet Manager, accessible from the "Cloud Setup" screen.

GCP authentication
=====================

Fleet Manager needs to perform various calls to the GCP API in order to manage resources.

When you deploy Cloud Stacks using the recommended guided setup, the Fleet Manager virtual machine has a service account, whose permissions it uses.

License
========

In order to benefit from most capabilities, you'll need a Dataiku License or Dataiku License Token. You need to enter it here.

HTTP proxy
==========

Fleet Manager can run behind a proxy. Once you define at least a proxy host and port, Fleet Manager will use it to access different resources through HTTP:

* to fetch new DSS image lists
* to update or verify licenses
* to log users in with the OpenID Connect protocol

The calls to GCP services won't be proxied. As such, please make sure the following GCP services you require are reachable from the Fleet Manager virtual machine: Cloud APIs, Cloud KMS, Cloud DNS.
You can for example use Private Service Connect to open access to GCP services in your network security group.