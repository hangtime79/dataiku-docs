Advanced security options
##########################

.. contents::
	:local:


Hiding error stacks
====================

By default, the DSS backend sends backend error stacks to logged-in users. This makes debugging and understanding easier.

This behavior can be disabled in the following way:

* Stop DSS

.. code-block:: bash

	DATADIR/bin/dss stop

* Edit the ``DATADIR/config/general-settings.json`` file
* Locate the ``"security"`` top-level key in the JSON file. If it does not exist, create it as an empty JSON object

* Within "security", add or edit the following key : ``"hideErrorStacks" : true``

* Start DSS

.. code-block:: bash

	DATADIR/bin/dss start


Hiding version info
====================

By default, the DSS backend sends DSS version information, even to non-logged in users.

This behavior can be disabled in the following way:

* Stop DSS

.. code-block:: bash

	DATADIR/bin/dss stop

* Edit the ``DATADIR/config/general-settings.json`` file
* Locate the ``"security"`` top-level key in the JSON file. If it does not exist, create it as an empty JSON object

* Within "security", add or edit the following key : ``"hideVersionStringsWhenNotLogged" : true``

* Start DSS

.. code-block:: bash

	DATADIR/bin/dss start


Using secure cookies
=====================

By default, DSS login cookies do not carry the ``Secure`` flag (which would make them unusable over non-secured HTTP connections).

If you configure DSS to using HTTPS for all users, either :ref:`natively <config.https>` or through a :doc:`reverse proxy </installation/custom/reverse-proxy>`,
you can enable the use of secure cookies.
This further secures user connections by ensuring the browser never sends the session cookie over unsecured connections.

* Stop DSS

.. code-block:: bash

	DATADIR/bin/dss stop

* Edit the ``DATADIR/config/general-settings.json`` file
* Locate the ``"security"`` top-level key in the JSON file. If it does not exist, create it as an empty JSON object

* Within "security", add or edit the following key : ``"secureCookies" : true``

* Start DSS

.. code-block:: bash

	DATADIR/bin/dss start

Expiring sessions
==================

DSS version ≥ 14.3.0
--------------------------

By default, DSS sessions expire after 30 days of inactivity. You can configure DSS to have sessions expire after a certain amount of time since login, and/or after a certain amount of inactivity.

.. warning::

	* Sessions expiration can cause lost work: if you have work open and your session expires, you may not be able to save your work

	* If you have a Jupyter notebook open and your session expires, the underlying Jupyter kernel remains alive and you can still communicate with it and execute code, until the next page refresh. However, saving updates to the notebook becomes impossible


* In DSS, go to Administration > Settings > Security & Audit > User login & provisioning > Session management
* Set the "Maximum session duration" and "Idle timeout" options to the desired expiration timeout, respectively since login and inactivity.
* Save (restart is not needed)

If session expiration was previously configured using the method for DSS < 14.3.0, it is recommended to remove the key ``dku.sessions.storage=memory`` from the ``DATADIR/config/dip.properties`` file because using non-persistent session storage is no longer necessary to enable session expiration.
It is still possible to re-enable non-persistent session storage if desired by unchecking the "Session persistence" option on the same page.

DSS version < 14.3.0
--------------------------

By default, DSS sessions do not expire. You can configure DSS to have sessions expire, either after a certain amount of time since login, or after a certain amount of inactivity.

.. warning::

	* Enabling sessions expiration also means that all user sessions are always terminated each time the DSS backend restarts

	* Sessions expiration can cause lost work: if you have work open and your session expires, you may not be able to save your work

	* If you have a Jupyter notebook open and your session expires, the underlying Jupyter kernel remains alive and you can still communicate with it and execute code, until the next page refresh. However, saving updates to the notebook becomes impossible

* Stop DSS

.. code-block:: bash

	DATADIR/bin/dss stop

* Edit the ``DATADIR/config/dip.properties`` file and add the following key: ``dku.sessions.storage=memory``

* Edit the ``DATADIR/config/general-settings.json`` file
* Locate the ``"security"`` top-level key in the JSON file. If it does not exist, create it as an empty JSON object

* Within "security", add or edit the following keys: ``"sessionsMaxTotalTimeMinutes"`` and ``"sessionsMaxIdleTimeMinutes"``. Set them to the desired expiration timeout, respectively since login and on inactivity. 0 means no expiration for this kind.

* Start DSS

.. code-block:: bash

	DATADIR/bin/dss start


Forcing a single session per user
==================================

By default, DSS users can log in from multiple sessions at once. You can additionally configure DSS to only allow a single session. When a user logs in, all their other sessions are terminated.

DSS version ≥ 14.3.0
--------------------------

* In DSS, go to Administration > Settings > Security & Audit > User login & provisioning > Session management
* Check the "Force single session per user" option to enable it
* Save (restart is not needed)

DSS version < 14.3.0
--------------------------

* Stop DSS

.. code-block:: bash

	DATADIR/bin/dss stop

* Edit the ``DATADIR/config/general-settings.json`` file
* Locate the ``"security"`` top-level key in the JSON file. If it does not exist, create it as an empty JSON object

* Within "security", add or edit the following key : ``"forceSingleSessionPerUser" : true``

* Start DSS

.. code-block:: bash

	DATADIR/bin/dss start


Restricting visibility of groups and users
============================================

By default, all logged-in DSS users can view the list of groups and users. This is useful for:

* Allowing project owners to add groups to their projects
* Allowing users to mention all users

You can select to restrict visibility of groups and users. The following rules apply:

* If you are admin, you can see everything
* You can see all groups to which you belong
* You can see all users of groups to which you belong
* In addition, you can see all users that are participants in projects in which you are participant

Instructions:

* Stop DSS

.. code-block:: bash

	DATADIR/bin/dss stop

* Edit the ``DATADIR/config/general-settings.json`` file
* Locate the ``"security"`` top-level key in the JSON file. If it does not exist, create it as an empty JSON object

* Within "security", add or edit the following key : ``"restrictUsersAndGroupsVisibility" : true``

* Start DSS

.. code-block:: bash

	DATADIR/bin/dss start


.. note::

	This is a best-effort feature. Obvious listing of users are suppressed, but we do not guarantee perfect isolation.


Redirecting to a custom URL after logout
=========================================

By default, when users log out from DSS, they are redirected to a standard Web page hosted by DSS.

To configure DSS to redirect users to a different URL when they log out:

* Stop DSS

.. code-block:: bash

	DATADIR/bin/dss stop

* Edit the ``DATADIR/config/general-settings.json`` file
* Locate the ``"security"`` top-level key in the JSON file. If it does not exist, create it as an empty JSON object

* Within "security", add the following keys: 

.. code-block:: javascript

        "postLogoutBehavior": "CUSTOM_URL",
        "postLogoutCustomURL": "https:///my-custom-url"


* Start DSS

.. code-block:: bash

	DATADIR/bin/dss start


Example general-settings.json file
===================================

With the previous options enabled, your general-settings.json could look like:

.. code-block:: json

	{
	  "udr": true,
	  "proxySettings": {
	    "port": 0
	  },
	  "mailSettings": {},
	  "maxRunningActivitiesPerJob": 5,
	  "maxRunningActivities": 5,
	  "ldapSettings": {
	    "enabled": false,
	    "useTls": false,
	    "userFilter": "(\u0026(objectClass\u003dposixAccount)(uid\u003d{USERNAME}))",
	    "displayNameAttribute": "cn",
	    "emailAttribute": "mail",
	    "enableGroups": true,
	    "groupFilter": "(\u0026(objectClass\u003dposixGroup)(memberUid\u003d{USERNAME}))",
	    "groupNameAttribute": "cn",
	    "autoImportUsers": true
	  },
	  "computablesAvailabilityMode": "EXPOSED_ONLY",
	  "globalCrossProjectBuildBehaviour": "STOP_AT_BOUNDARIES",
	  "noLoginMode": false,
	  "sessionsMaxTotalTimeHours": 0,
	  "sessionsMaxIdleTimeHours": 0,
	  "security" : {
	    "hideVersionStringsWhenNotLogged" : true,
	    "hideErrorStacks" : true,
	    "secureCookies" : true,
	    "sessionsMaxTotalTimeMinutes": 0,
	    "sessionsMaxIdleTimeMinutes": 20,
	    "forceSingleSessionPerUser": false,
	    "restrictUsersAndGroupsVisibility": true,
	    "postLogoutBehavior": "CUSTOM_URL",
	    "postLogoutCustomURL": "https://www.dataiku.com"
	  }
	}

.. _advanced-options.restricted-types-wikis:

Restricting types of files that can be uploaded in wikis
========================================================

By default, all logged-in DSS users can upload any type of files to wiki articles.

You can configure DSS to restrict the types of files that are allowed by specifying a list of accepted extensions.

* Edit the ``DATADIR/config/dip.properties`` file
* Add ``dku.wikis.authorizedUploadExtensions=png,jpg,jpeg,gif,txt,csv`` (update the list according to your security needs)


Restricting exports
=====================

It is possible to globally restrict some export features in DSS (regardless of project permissions).

.. warning::

	Any restriction to exports conceptually remains a "best-effort". Any user who is granted the right to see data
	in DSS can, with more or less effort, manage to export it, if only by copy/pasting it.


To use these options, a DSS administrator with access to the DSS server needs to edit the "config/dip.properties" file in the DSS data dir and add one of the following lines:

* ``dku.exports.disableAllDatasetExports=true``
	* Disables exports of datasets globally on the instance (the exports that are restricted are the ones that are about "Download" of datasets in order to generate data files (CSV, Excel, Tableau Hyper, ...).
	* Other exports (ML data, schema, SQL queries, prepared data) remain possible
	* Disables ability to include datasets in project exports and bundle downloads
	* Disables ability to attach datasets to emails in scenarios

* ``dku.exports.disableAllDataExports=true`` (implies the previous one)
	* Disables exports of datasets globally on the instance (the exports that are restricted are the ones that are about "Download" of datasets in order to generate data files (CSV, Excel, Tableau Hyper, ...). 
	* Disables exports of prepared data or SQL query results
	* Exports of ML data and schemas remain possible
	* Disables ability to download files of zips from managed folders
	* Disables ability to include datasets or managed folders in project exports and bundle downloads
	* Disables ability to attach datasets or other data items to emails in scenarios

* ``dku.exports.disableAllExports=true`` (implies the previous one)
	* Disables exports of datasets globally on the instance (the exports that are restricted are the ones that are about "Download" of datasets in order to generate data files (CSV, Excel, Tableau Hyper, ...). 
	* Disables exports of prepared data or SQL query results
	* Disables exports of ML data and schemas
	* Disables ability to download files of zips from managed folders
	* Disables ability to include datasets or managed folders in project exports and bundle downloads
	* Disables ability to attach datasets or other data items to emails in scenarios

Setting security-related HTTP headers
======================================

It is possible to set the following security-related HTTP headers:

* X-Frame-Options
* Content-Security-Policy
* X-XSS-Protection
* X-Content-Type-Options
* Strict-Transport-Security
* Referrer-Policy
* Permissions-Policy
* Cross-Origin-Embedder-Policy
* Cross-Origin-Opener-Policy
* Cross-Origin-Resource-Policy

All of these are configured in the ``[server]`` section of the ``install.ini`` file.

Here is a syntax example:

.. code-block:: ini

	[server]
	port=11000

	content-security-policy=script-src 'self' 'unsafe-inline' 'unsafe-eval'; frame-ancestors 'none'
	x-frame-options=SAMEORIGIN
	x-content-type-options=nosniff
	x-xss-protection=1;mode=block
	hsts-max-age=31536000
	referrer-policy=same-origin
	permissions-policy=fullscreen
	cross-origin-embedder-policy=unsafe-none 
	cross-origin-opener-policy=unsafe-none
	cross-origin-resource-policy=cross-origin	


You need to run ``./bin/dssadmin regenerate-config`` and to restart DSS after changing this.

Allowing DSS to be hosted inside an iframe
===========================================

By default, DSS cannot be hosted inside an iframe as Web browsers treats its authentication cookies as SameSite=Lax.

To configure DSS to emit authentication cookies using SameSite=None:

* Stop DSS

.. code-block:: bash

	DATADIR/bin/dss stop

* Edit the ``DATADIR/config/general-settings.json`` file
* Locate the ``"security"`` top-level key in the JSON file. If it does not exist, create it as an empty JSON object

* Within "security", add or edit the following keys: ``"sameSiteNoneCookies" : true`` and ``"secureCookies" : true``

* Start DSS

.. code-block:: bash

	DATADIR/bin/dss start

.. note::

	DSS must be accessed via the HTTPS protocol and cookies must be set as Secure for this option to work as
	Web browsers do not take into account the SameSite cookie parameter for non-secure cookies.

Preventing links to be clickable in data tables
===============================================
By default, links are displayed in dataset Explore and dataset insights.

To prevent this, edit the ``DATADIR/config/dip.properties`` file and add the following key: ``dku.feature.dataTableLinks.enabled=false``

Allowing DSS users to edit their display names and emails
=============================================================

Starting from version 13.2.0, users can no longer edit their display names and email addresses. Only DSS administrators have the ability to make these changes. This restriction helps prevent impersonation by DSS users.

To allow users to update their display names and email addresses:

* Stop DSS

.. code-block:: bash

	DATADIR/bin/dss stop

* Edit the ``DATADIR/config/general-settings.json`` file

* Locate the ``"security"`` top-level key in the JSON file. If it does not exist, create it as an empty JSON object

* Within "security", add or edit the following keys: ``"enableEmailAndDisplayNameModification" : true``.

* Start DSS

.. code-block:: bash

	DATADIR/bin/dss start

.. note::

	Please note that enabling email and display name modifications will disable the ability for users to share assets, such as projects, via email invitations.
