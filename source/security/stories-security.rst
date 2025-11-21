Stories security
###################

.. contents::
	:local:

.. note::
    Note that Dataiku Stories is not available in all Dataiku licenses. You may need to reach out to your Dataiku Account Manager or Customer Success Manager.
    

Authentication
=================

Stories does not handle authentication by itself. 

Instead, it uses the DSS cookie, so a user must first authenticate to DSS.

Authorization
================

Stories checks user authorizations against DSS workspaces.

When a user has read access to a workspace, he can read any story in the workspace.

When a user has write access to a workspace, he can write any story in the workspace.

Internal databases credentials
================================

Credentials of Stories internal databases (redis, mongodb, clickhouse) are generated and used in the Stories docker container only.

They are not accessible by DSS or any process outside of Stories.

Audit trail
==============

Stories currently logs the following events in the DSS audit trail:

* story-datastory-get: logs a story read access
* story-datastory-get-members: logs a request to list active users on a story

