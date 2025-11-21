Setting up the Deployer
########################

.. contents::
	:local:

There are two modes for installing the Deployer:

* **Local Deployer.**  When your infrastructure has a single Design or Automation node that you will use to create API services and/or projects, the Deployer can be part of this DSS node itself - in that case, no additional setup is required.
* **Standalone Deployer.** When your infrastructure includes multiple Design and/or Automation nodes that you will use to create API services and/or projects, you can install a separate DSS node which will act as the centralized Deployer for all Design and Automation nodes.

Using a local Deployer
============================

When you install a DSS Design or Automation node, it is already preconfigured with its own Deployer.

You can skip to the :ref:`apinode.installing-apideployer.apideployer-first-infrastructure` section for the API Deployer or the :ref:`bundles.installing-projectdeployer.projectdeployer-first-infrastructure` section for the Project Deployer.

Using a standalone Deployer
============================

* If you are using Dataiku Cloud Stacks for AWS, you simply need to create a new instance of type Deployer
* If you are using Dataiku Cloud, you simply need to activate the automation or API node in your launchpad (extension tab). The instance and the deployer will be automatically created and managed.
* If you are using Dataiku Custom, please see :doc:`/installation/custom/deployer-node`

Setup users
------------

The whole security mechanism of the Deployer is based on the *matching of user logins* between the various nodes. It is thus critical that the same users with the same logins exist on the Deployer node. Otherwise, your Design or Automation users won't be able to publish to the Deployer, or deploy to the Automation node in the case of the Project Deployer.

You therefore need to setup users access on the Deployer in a similar fashion to your Design and Automation nodes.

If you are using LDAP logins for your Design and Automation nodes, remember that the default behavior is to import users dynamically from LDAP the first time they connect to DSS (provided that they belong to an authorized group). This import is only done when logging on the DSS node, so before being able to push services to the Deployer, users will need to login at least once on the Deployer node.

Connect your Design and Automation instances
----------------------------------------------

.. note::

	If you are using Dataiku Cloud Stacks, and have enabled fleet management on your virtual network, this is done automatically, you don't need to do these operations.

Next, you are going to configure:

* your Design nodes so that they can publish their projects and/or API services to the Deployer
* your Automation nodes so that they can publish API services to the Deployer

Generate an admin API key on the Deployer
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

On the Deployer, go to Administration > Security > Global API keys and generate a new API key. This key must have global admin privileges. Take note of the secret.

Setup the key on the Design / Automation nodes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

On the Design or Automation node:

* Go to Administration > Settings > Deployer
* Set the Deployer mode to "Remote" to indicate that we'll connect to another node
* Enter the base URL (:samp:`https://[host]:[port]`) of the Deployer node that you installed
* Enter the secret of the API key

Repeat for each Design or Automation node that you wish to connect to the Deployer.
