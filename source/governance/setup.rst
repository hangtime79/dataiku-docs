Govern Instance Setup
#####################

.. contents::
	:local:


Installing Govern
=================

There are two modes for installing Govern:

* If you are using :doc:`Dataiku Cloud Stacks </installation/cloudstacks-aws/index>` , you simply need to create a new instance of type Govern.

* If you are using Dataiku Custom, please refer to :doc:`/installation/custom/govern-node`.

User setup and authentication
=============================

It is recommended to have the same user logins between the different nodes of your Dataiku cluster. Users management on Govern node is the same as on other node types. Please see :doc:`/security/index` for more details.


Connecting your Govern and Design, Automation or Deployer instances
===================================================================

.. warning::
        We recommend that you keep the versions of the nodes connected to Govern in sync with the version of the Govern node.
        
	Although it may work, connecting nodes to Govern with different software versions is not supported.

.. note::

	If you are using Dataiku Cloud Stacks, and have enabled fleet management on your virtual network, this is done automatically, so you don't need to do the following operations.

Next, you are going to configure:

* your Design / Automation nodes so that the different objects (projects, models, model versions) can be published to Govern
* your Deployer nodes so that they can check the governance status of projects or API services before deploying them

Setting up your node IDs
%%%%%%%%%%%%%%%%%%%%%%%%

For the Govern integration to work properly, you have to set the node ID of every DSS node that will connect to Govern.

You can configure a node ID by adding a :samp:`nodeid` configuration option to the :samp:`general` section of the :samp:`DATADIR/install.ini` file, as shown in the example below:

.. code-block:: ini

        [general]
        nodeid = YOUR_NODE_ID

After modifying that file, you will have to restart the DSS node in question.

You also have to make Govern aware of the node IDs you configured. In Govern, go to "Administration > Settings > Notifications & Integrations" and add an entry per node to the "Fallback node references" section.

Generate an admin API key on Govern
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

On Govern, go to Administration > Security > Global API keys and generate a new API key. This key must have global admin privileges. Take note of the secret.

Setup the key on the Design / Automation / Deployer nodes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

On the Design, Automation or Deployer node:

* Go to "Administration > Settings > Dataiku Govern"
* Enable Dataiku Govern integration
* Enter the base URL (:samp:`http(s)://[host]:[port]`) of the Govern node that you installed
* Enter the secret of the API key

Repeat for each Design / Automation / Deployer node that you wish to connect to Govern.

Making Govern aware of its external URL
=======================================

As any other node type, Govern cannot guess what its external URL is.

The external URL is used any time Govern needs to build an absolute URL for the user, for example when sending links to Govern in an :ref:`email <governance.email>`.

To configure this setting, go to "Administration > Settings > Notifications & Integrations" and click on the wand icon: it should automatically set the Govern external URL by looking at the current URL of your browser.

Defining the Govern instance name
=================================

You can set the name of your Govern node by going to "Administration > Settings > Instance".

If you set an instance name, it will be displayed at the top right of every page of this instance, in the main navigation bar.

When defined, the instance name will also be included in audit trail messages when they are sent to an :doc:`event server </operations/audit-trail/eventserver>`.

.. _governance.email:
   
Setting up email notifications
==============================

Govern can be configured to send email notifications when appropriate. Currently, this is mostly used to notify users about changes in the :ref:`sign-off status of an item <sign-off>`.

To enable email notifications:

* Go to "Administration > Settings > Notifications & Integrations".
* Enable the "Enable notification emails" checkbox.
* Fill-in the SMTP server connection parameters (host, port, SSL, TLS, login, password).
* Click "Save"
 
In addition, you must make sure that users who wishes to receive email notifications have their email address correctly set in their user profiles.

Managing security
=================

Please see :doc:`/security/govern-permissions` for details on the Govern security model.
