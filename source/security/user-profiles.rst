User profiles
#########################

.. contents::
    :depth: 2
    :local:

Each user in DSS has a single "user profile" assigned to it.

.. note::

	User profile is **not a security feature**, but a licensing-related concept. DSS licenses are restricted in number of each profile.

	We do not provide any guarantee that the user profile is strictly applied. 

	For security, use the regular groups authorization model described in this documentation. Do not use user profiles to implement any kind of security.


Depending on your Dataiku license, various user profiles may be available. The exact definition of user profiles that are available depends on your DSS license. In case of any doubt, please contact your Dataiku Account Manager. You may have other profiles available, or only some of them.

Some of the possible profiles are:

* **Full Designer**: Full Designers have access to all Dataiku features.

* **Data Designer**: Data Designers have access to most visual features, but not to coding (Python/R) features, nor to some advanced AI and ML features.

* **Advanced Analytics Designer**: Advanced Analytics Designers have access to most features, except some advanced coding capabilities.

* **Governance Manager**: Governance Managers can view projects in Dataiku and handle artifacts and sign-off processes in Dataiku Govern.

* **AI Consumer**: AI Consumers can access dashboards, workspaces, webapps, as well as run :doc:`Dataiku Applications </applications/index>` that Designers have created.

* **AI Access User**: AI Access Users can only access webapps that have been made available to them, such as :doc:`/agents/agent-hub`.

* **Technical Account**: Technical Accounts technically have access to all Dataiku features, but may only perform administration / assistance tasks, not productive work. Technical Accounts can also be used as service accounts to run scenarios or webapps.


Some of the older available profiles (which you may have access to if you are an older Dataiku customer) include:

* **Designer**: Designers have full access to all Dataiku features.

* **Data Scientist**: Same as Designer.

* **Data Analyst**: Data Analysts have access to most visual features, but not to coding features nor to AI and ML features.

* **Reader**: Readers can read the content of projects but cannot perform any kind of modification. They can access dashboards and webapps.

* **Explorer**: Explorers have the capabilities of readers, and they can also run :doc:`Dataiku Applications </applications/index>` that Designers have created. They can also create their own dashboards and insights, but only based on existing datasets/models/...

* **Platform Admin**: Platform Admins technically have access to all Dataiku features, but may only perform administration / assistance tasks, not productive work. Note that despite the name, granting the Platform Admin user profile does not automatically grant administration rights.


Other profiles may be available, and not all of these may be available. Please contact your Dataiku Account Manager for any further information.