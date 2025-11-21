Guided setup 1: Deploy in a new VNet with Elastic Compute
#########################################################

.. toctree::

.. contents::
    :local:

Description
===========

This guided setup allows you to setup a full Dataiku Cloud Stacks for Azure setup, including the ability to run workloads on Elastic Compute clusters powered by Kubernetes (using Azure AKS).

At the end of this setup, you'll have:

* A fully-managed DSS design node, with either a public IP or a private one
* The ability to one-click create elastic compute clusters
* The elastic compute clusters running with public IPs (and no NAT gateway overhead)


Prerequisites
=============

You need to have, as an administrator, the `Owner` role on the resource group. Ownership is required to give permissions to the managed identities used
by the software at runtime. Said identities do not require to have the role `Owner` themselves. `Owner` privileges are only used by the administrator
for initial setup and is not required by the software during usage.

For the following steps, we assume an ACR (Azure Container Registry) is created and available in your resource group.

Steps
======

Create a managed identity for your Fleet Manager instance
---------------------------------------------------------

* In your Microsoft Azure portal, click on "Create a resource"

* Search for "User Assigned Managed Identity"

* Click on create

* Select the correct subscription and resource group

* Select the region

* Enter a name for your managed identity, this will be referred as ``fm-id-name``

* Click on "Review + Create", then on "Create"

* When your deployment is ready, click on "Go to resource"

* Click on "Azure role assignments", then "Add role assignment"

* For the "Scope", select "Resource group"

* Select the correct subscription and resource group

* For the "Role" select "Contributor"

* Click on "Save"

* Go to the "Properties" tab and copy the "Resource ID", this will be refered as ``fm-id``


Create a managed identity for your DSS instances
------------------------------------------------

Reproduce the exact same step as above (i.e. the steps for the Fleet Manager managed identity) for the DSS managed identity.
We will refer to its name by ``dss-id-name`` and to its "Resource ID" by ``dss-id``

As a consequence of role assignments inheritance, this identity is also `Contributor` on the ACR.


Deploy Fleet Manager
--------------------

Click the following link to deploy the Fleet Manager and all needed resources from the Azure portal:

.. image:: img/azure-deploy.png
    :alt: Deploy to Azure
    :target: https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fdkutemplates.blob.core.windows.net%2Ffleet-manager-templates%2F14.2.2%2Ffleet-manager-network.json

In the portal fill the required information for the deployment:

* Choose the target subscription

* Choose an existing resource group or create a new one

* Select the region where the resource should be deployed

* Select the size of the Virtual machine

* In "Instance identity", enter the ``fm-id-name``

* In "Username", choose a username for logging in to Fleet Manager

* In "Password", enter a strong password for logging in to Fleet Manager

* In "SSH Username", choose a username for logging in to the underlying Fleet Manager virtual machine (it is not normally required)

* In "SSH public key source", enter a RSA public key for SSH logging in to the underlying Fleet Manager virtual machine (it is not normally required)

* In "Virtual Network CIDR", enter a /16 CIDR, for example ``10.0.0.0/16``

* In "Subnet CIDR", enter a CIDR included in the chosen Virtual Network CIDR, for example ``10.0.1.0/24``

* In "Secondary subnet CIDR", enter a CIDR included in the chosen Virtual Network CIDR that does not overlap with the previously chosen Subnet CIDR, for example ``10.0.2.0/24``

* In "Associate Public Ip Address", select whether you want a public IP to connect to Fleet Manager

* In "Resources Tags", you can optionally add tags that you would like to be applied to the resources deployed. They must be valid according to Azure guidelines. Example:

.. code-block::

  {
    "tag_key": "tag_value",
    "tag_novalue": ""
  }

* Click on "Review + create"

* Verify the creation information, then click on "Create"

* Wait for your deployment to appear as completed

* Click on "Go to resource group"

* Click on the Virtual Machine

* Copy the "Public IP address"

This is the address at which your Cloud Stacks Fleet manager is deployed. Open a new tab to this address and wait for the login screen to appear.

Start your first DSS
--------------------

* Log into Fleet Manager with the login and the password you previously entered

* In "Cloud Setup", click on "Edit", set "License mode" to "Manually entered", click on "Enter license" and enter your Dataiku license. Click on "Done" then on "Save"

* Refresh the page in your browser

* In "Fleet Blueprints", click on "Elastic Design"

* Give a name to your new fleet, this will be referred to as ``fleet-name``

* In "Authorized SSH Key", enter your RSA public key

* In "Instance managed identity", enter the ``dss-id``

* Click on "Deploy"

* Go to "Instances > All", click on the design node

* Click "Provision"

* Wait for your DSS instance to be ready

* Click on "Retrieve password" and write-down the password

* Click on "Go to DSS"

* Login with "admin" as the login, and the password you just retrieved

You can now start using DSS

(Optional) Start your first Elastic compute cluster
---------------------------------------------------

Deploy your Elastic Compute cluster
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

* In DSS, go to Administration > Clusters

* Click on "Create AKS cluster", give it a name

* In "Credentials", check it is set to "Manually defined" -> "Default credentials, from environment"

* In section "Identity assumed by cluster components", check it is set to "Manually defined" -> "Managed identities". The option "Inherit DSS identity" should
  be checked.

* In "Cluster Nodes", Click on "+ Add a preset"

* Update "Machine type" and "Disk size" as you see fit

* Tick the "Enable nodes autoscaling" box

* Untick the "Availability zones" option in "Networking" section of the node pool.

* In "Service CIDR" add a CIDR for your cluster, it should not overlap ``10.0.0.0/16``. For example: ``10.1.0.0/16``

* In "DNS IP", set an IP for the DNS, in your specified CIDR range. For example: ``10.1.0.10``

* Click on "Start"

* Wait for your cluster to be available

* In Settings, go to "Containerized execution", and in "Default cluster", select the cluster you just created.

* Click on "+ Add another config"

* In "Configuration name" add a name

* In "Image registry url" enter ``acr-name``.azurecr.io

* In "Image pre-push hook", select "Enable push to ACR"

* Click on "Save" then "Push base images". When finished, click on "(Re)Install Jupyter kernels".

* In a project, you can now use containerized execution for any activity, using the containerized config you created


Troubleshooting
===============

"Tenant ID, application ID, principal ID, and scope are not allowed to be updated (code: RoleAssignmentUpdateNotPermitted)"
---------------------------------------------------------------------------------------------------------------------------

This error is known to happen whenever a new stack is deployed in a resource group in which an existing stack have been deleted.
The most likely reason is some role assignments were left over and must be deleted before you can deploy again.

* In your Microsoft Azure portal, display your resource group, then click on "Access Control (IAM)"

* Select the "Role assignments" tab in the right blade.

* Find all the entries with name "Identity not found" and scope "This resource" and select them.

* Click on the "Remove" button at the top of the blade.

* You can then redeploy the ARM template. No need to delete the resources which creation succeeded, just redeploy it like you did before the failure.

"The requested identity has not been assigned to this resource"
---------------------------------------------------------------

This error means you instructed DSS to authenticate with a specific User Assigned Managed Identity but this specific identity
has not been assigned to the machine. Check your instance template for correct assignment of the desired identity, and reprovision
if the error persists.
