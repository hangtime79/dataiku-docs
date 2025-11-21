:tocdepth: 3

Fleet Manager
#############

For usage information and examples, see :doc:`/concepts-and-examples/fleetmanager/index`.

The main FMClient class
=======================

.. autoclass:: dataikuapi.fmclient.FMClient
.. autoclass:: dataikuapi.fmclient.FMClientAWS
.. autoclass:: dataikuapi.fmclient.FMClientAzure
.. autoclass:: dataikuapi.fmclient.FMClientGCP

Fleet Manager Accounts
=======================

.. autoclass:: dataikuapi.fm.cloudaccounts.FMCloudAccount
.. autoclass:: dataikuapi.fm.cloudaccounts.FMCloudAccountCreator
.. autoclass:: dataikuapi.fm.cloudaccounts.FMAWSCloudAccount
.. autoclass:: dataikuapi.fm.cloudaccounts.FMAWSCloudAccountCreator
.. autoclass:: dataikuapi.fm.cloudaccounts.FMAzureCloudAccount
.. autoclass:: dataikuapi.fm.cloudaccounts.FMAzureCloudAccountCreator
.. autoclass:: dataikuapi.fm.cloudaccounts.FMGCPCloudAccount
.. autoclass:: dataikuapi.fm.cloudaccounts.FMGCPCloudAccountCreator

Fleet Manager Instances
=======================

.. autoclass:: dataikuapi.fm.instances.FMInstance
.. autoclass:: dataikuapi.fm.instances.FMInstanceCreator
.. autoclass:: dataikuapi.fm.instances.FMAWSInstance
.. autoclass:: dataikuapi.fm.instances.FMAWSInstanceCreator
.. autoclass:: dataikuapi.fm.instances.FMAzureInstance
.. autoclass:: dataikuapi.fm.instances.FMAzureInstanceCreator
.. autoclass:: dataikuapi.fm.instances.FMGCPInstance
.. autoclass:: dataikuapi.fm.instances.FMGCPInstanceCreator
.. autoclass:: dataikuapi.fm.instances.FMInstanceEncryptionMode
.. autoclass:: dataikuapi.fm.instances.FMInstanceStatus
.. autoclass:: dataikuapi.fm.instances.FMSnapshot

Fleet Manager Virtual Networks
==============================

.. autoclass:: dataikuapi.fm.virtualnetworks.FMVirtualNetwork
.. autoclass:: dataikuapi.fm.virtualnetworks.FMVirtualNetworkCreator
.. autoclass:: dataikuapi.fm.virtualnetworks.FMAWSVirtualNetwork
.. autoclass:: dataikuapi.fm.virtualnetworks.FMAWSVirtualNetworkCreator
.. autoclass:: dataikuapi.fm.virtualnetworks.FMAzureVirtualNetwork
.. autoclass:: dataikuapi.fm.virtualnetworks.FMAzureVirtualNetworkCreator
.. autoclass:: dataikuapi.fm.virtualnetworks.FMGCPVirtualNetwork
.. autoclass:: dataikuapi.fm.virtualnetworks.FMGCPVirtualNetworkCreator
.. autoclass:: dataikuapi.fm.virtualnetworks.FMHTTPSStrategy

Fleet Manager Instance Templates
================================

.. autoclass:: dataikuapi.fm.instancesettingstemplates.FMInstanceSettingsTemplate
.. autoclass:: dataikuapi.fm.instancesettingstemplates.FMInstanceSettingsTemplateCreator
.. autoclass:: dataikuapi.fm.instancesettingstemplates.FMAWSInstanceSettingsTemplateCreator
.. autoclass:: dataikuapi.fm.instancesettingstemplates.FMAzureInstanceSettingsTemplateCreator
.. autoclass:: dataikuapi.fm.instancesettingstemplates.FMGCPInstanceSettingsTemplateCreator
.. autoclass:: dataikuapi.fm.instancesettingstemplates.FMSetupAction
.. autoclass:: dataikuapi.fm.instancesettingstemplates.FMSetupActionStage
.. autoclass:: dataikuapi.fm.instancesettingstemplates.FMSetupActionAddJDBCDriverDatabaseType

Fleet Manager Load Balancers
============================

..autoclass:: dataikuapi.fm.loadbalancers.FMLoadBalancer
..autoclass:: dataikuapi.fm.loadbalancers.FMLoadBalancerCreator
..autoclass:: dataikuapi.fm.loadbalancers.FMLoadBalancerPhysicalStatus
..autoclass:: dataikuapi.fm.loadbalancers.FMAWSLoadBalancer
..autoclass:: dataikuapi.fm.loadbalancers.FMAWSLoadBalancerCreator
..autoclass:: dataikuapi.fm.loadbalancers.FMAzureLoadBalancer
..autoclass:: dataikuapi.fm.loadbalancers.FMAzureLoadBalancerCreator
..autoclass:: dataikuapi.fm.loadbalancers.FMAzureLoadBalancerTier

Fleet Manager Tenant
====================

.. autoclass:: dataikuapi.fm.tenant.FMCloudAuthentication
.. autoclass:: dataikuapi.fm.tenant.FMCloudCredentials
.. autoclass:: dataikuapi.fm.tenant.FMCloudTags

Fleet Manager Future
====================

.. autoclass:: dataikuapi.fm.future.FMFuture
