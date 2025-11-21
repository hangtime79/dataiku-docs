Configuring LDAP authentication
###############################

.. contents::
    :local:

.. note::

  LDAP authentication is a license-controlled feature.

.. note::

  DSS LDAP implementation is an Authenticator and a User Supplier. See :doc:`Authentication </security/authentication/index>` documentation for more details.

Data Science Studio can authenticate users against an external LDAP directory
in addition to its built-in user database. Most corporate directories provide LDAP
authentication service, including Microsoft Active Directory. This enables integration of
user and password management, as well as user rights assignment, with existing
centrally-managed infrastructures.

To configure LDAP authentication, you first need to gather and provide technical information about your
directory service (see :ref:`ldap.connecting`):

* Basic connection information to your LDAP server (host name and port, credentials,
  connection security).
* A filter (LDAP query template) defining the subset of your directory corresponding to users
  authorized to access this DSS instance.
* Optionally, another filter defining the groups to which a given user belongs, in order to
  further restrict login authorization (only members of these groups being authorized to access
  this DSS instance) or to define user rights within DSS.

You can then choose to have Data Science Studio automatically import valid LDAP user accounts on
first login, or disable this feature and create DSS accounts for specific LDAP users only
(see :ref:`ldap.users`):

* when automatic provisioning is enabled (the default): once a DSS administrator has configured LDAP user
  mapping and authorization information as defined above, any LDAP user account matching the filter
  and authorization groups can access this DSS instance using his/her LDAP username and password,
  without further intervention of the administrator.
* if disabled: a DSS administrator configures LDAP user mapping and authorization
  information as defined above, and individually creates in DSS the user accounts which should be
  mapped to the LDAP directory. The corresponding users may then access this DSS instance using their
  LDAP username and password.
* In both cases, deleting or disabling an account in the LDAP directory automatically disables the
  corresponding DSS account.

It is possible to assign a user profile for newly imported users. You can also set this parameter per group (see :ref:`ldap.groups`)

You can finally define DSS groups which are automatically mapped to LDAP groups
(see :ref:`ldap.groups`), or add LDAP users to locally-defined DSS groups. These groups control user
access to DSS administrative rights, as well as their access level to DSS projects (read-only,
read-write, or no access). Changing group membership in the LDAP directory automatically updates
the corresponding DSS access rights on next login.

When LDAP authentication is enabled, the login sequence to Data Science Studio is the following:

* A user enters his/her username and password on Data Science Studio login page.
* If the username is found in the DSS account database and is of type LOCAL, the provided password is
  validated against the local database password.
* If the username is found in the DSS account database and is of type LDAP, or if the username is not
  found in the DSS account database and automatic account import is enabled, a corresponding LDAP
  user is searched in the directory using the configured filter.

  * if the LDAP user is found, its LDAP groups are searched in the directory using the configured
    group filter if any. Access is denied if the user is not found, or if authorization groups are
    configured and the user is a member of none.
  * the provided password is validated against the LDAP directory.
  * a new DSS account for this user is created if needed, initialized with information from the
    directory. Otherwise, DSS group membership information for this user is updated as needed to
    reflect current LDAP group membership for this user.

.. _ldap.connecting:

Connecting to a LDAP directory
------------------------------

To configure the connection to the LDAP directory:

* Go to the "Administration > Settings" page.
* Select "User login & provisioning" on the left hand column.
* Check the "Enable" check box on top of the LDAP section.
* Configure the required parameters as described below.
* You can test these parameters at any time using the "Test" button.
* Click on the "Save" button at the bottom of the left-hand column when done, or navigate out
  of the settings page to cancel.
* Optionally, configure DSS groups mapped to LDAP groups (see :ref:`ldap.groups`).
* Optionally, manually configure DSS users mapped to LDAP users (see :ref:`ldap.users`).

.. warning::

  You must be logged to DSS with administrator privileges.

Connection parameters
^^^^^^^^^^^^^^^^^^^^^

+-----------------+--------------------------------------------------------------------------+
|       Name      |                               Description                                |
+=================+==========================================================================+
| LDAP server URL | Defines the LDAP server to query, using syntax:                          |
|                 |                                                                          |
|                 | ``ldap[s]://HOST[:PORT]/BASE``                                           |
|                 |                                                                          |
|                 | This parameter is mandatory.                                             |
+-----------------+--------------------------------------------------------------------------+
| Use TLS         | Use StartTLS command to secure LDAP connection.                          |
|                 |                                                                          |
|                 | Valid for ldap url only, not ldaps.                                      |
+-----------------+--------------------------------------------------------------------------+
| Bind DN         | If the LDAP server requires authentication,                              |
|                 | specifies the DN to use for queries.                                     |
|                 |                                                                          |
|                 | If empty, DSS queries the LDAP server using anonymous bind.              |
+-----------------+--------------------------------------------------------------------------+
| Bind password   | If the LDAP server requires authentication,                              |
|                 | specifies the password to use for queries, along with the Bind DN above. |
|                 |                                                                          |
|                 | Mandatory if a Bind DN is specified.                                     |
+-----------------+--------------------------------------------------------------------------+

* The scheme of the server URL may be ldap:// to query the server using LDAP, or ldaps:// to query the server using LDAP over SSL
  (see :ref:`ldap.ssl`).
* The HOST part of the server URL specifies the hostname or IP address of the server to query. This part is mandatory.
* The PORT part of the server URL specifies an optional non-default network port. Default is 389 for ldap:// URLs and 636 for ldaps:// URLs.
* The BASE part of the server URL specifies the search base DN (Distinguished Name) to use for user and group queries. This part is mandatory.
  A valid URL would be for example: ``ldap://ldap1.company.com/OU=France,DC=company,DC=com``
* If "Use TLS" is enabled, the connection to the server will be secured using TLS encryption before sending queries.
  The server must support the "Start TLS" extension (see :ref:`ldap.ssl`).
* If the LDAP server allows anonymous binding, you can leave the "Bind DN" and "Bind password" fields empty. Otherwise,
  they specify credentials that DSS should use to authenticate with the LDAP server before sending queries.
* Note that DSS uses simple bind authentication when talking to the LDAP server, both to authenticate itself using the above
  credentials, and to verify user passwords. To avoid clear-text passwords being sent on the network, it is **strongly suggested**
  to use a secure channel between DSS and the LDAP server. Additional setup may be necessary in this case, see :ref:`ldap.ssl`.


User mapping parameters
^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------+--------------------------------------------------------------------------------------------------------------+
|          Name           |                                                 Description                                                  |
+=========================+==============================================================================================================+
| User filter by username | LDAP query template to use when searching a given username in the directory.                                 |
|                         |                                                                                                              |
|                         | This field is mandatory, and should be a valid LDAP query where the name to search is represented by         |
|                         | ``{USERNAME}``. This placeholder will be replaced by the username entered by the user on the DSS login page. |
|                         |                                                                                                              |
|                         | Upon success, this query should return exactly one LDAP object, representing the user in the directory.      |
+-------------------------+--------------------------------------------------------------------------------------------------------------+
| Display name attribute  | Optional attribute containing the user's full name (First Last) in the directory.                            |
|                         |                                                                                                              |
|                         | If specified, this attribute is retrieved to initialize the full name field of the DSS user account          |
|                         | when a LDAP account is automatically imported.                                                               |
+-------------------------+--------------------------------------------------------------------------------------------------------------+
| Email attribute         | Optional attribute containing the user's email in the directory.                                             |
|                         |                                                                                                              |
|                         | If specified, this attribute is retrieved to initialize the email field of the DSS user account              |
|                         | when a LDAP account is automatically imported.                                                               |
+-------------------------+--------------------------------------------------------------------------------------------------------------+

* Refer to :ref:`ldap.templates` for typical values of the above parameters in common setups.

Group mapping parameters
^^^^^^^^^^^^^^^^^^^^^^^^^

+--------------------------+-----------------------------------------------------------------------------------------------------------------+
|           Name           |                                                   Description                                                   |
+==========================+=================================================================================================================+
| Enable group support     | When enabled, DSS fetches the list of groups that the user belongs to from the directory                        |
|                          | using the parameters below. Otherwise, group-based authorization and LDAP group mapping                         |
|                          | are disabled.                                                                                                   |
+--------------------------+-----------------------------------------------------------------------------------------------------------------+
| Group filter by username | LDAP query template to use when searching the list of groups for a given user in the directory.                 |
|                          |                                                                                                                 |
|                          | This field is mandatory when group support is enabled. It should be a valid LDAP query where                    |
|                          | the user being looked up is represented by the ``{USERNAME}`` and/or ``{USERDN}`` placeholders.                 |
|                          |                                                                                                                 |
|                          | ``{USERNAME}`` is replaced by the username entered by the user on the DSS login page. ``{USERDN}`` is replaced  |
|                          | by the LDAP Distinguished Name (DN) of the user object returned by the "User filter" query above.               |
|                          |                                                                                                                 |
|                          | This query should return the list of LDAP group objects of which the user is a member.                          |
+--------------------------+-----------------------------------------------------------------------------------------------------------------+
| Group name attribute     | Name of the group object attribute containing the group name in the directory.                                  |
|                          |                                                                                                                 |
|                          | This field is mandatory when group support is enabled. It is the value of this attribute which is then          |
|                          | subsequently matched to the "Authorized groups" access list below, or when mapping LDAP groups to DSS groups.   |
+--------------------------+-----------------------------------------------------------------------------------------------------------------+
| Groups restriction       | List of LDAP group names, as returned by the "group filter" query fetching the "group name attribute" above.    |
|                          | Only users which are member of one of these groups are then authorized to connect to this DSS instance.         |
|                          |                                                                                                                 |
|                          | If this field is empty, no group-based authorization is performed. All LDAP users returned by the "User filter" |
|                          | query above can connect to this DSS instance.                                                                   |
+--------------------------+-----------------------------------------------------------------------------------------------------------------+

* Refer to :ref:`ldap.templates` for typical values of the above parameters in common setups.

On-demand provisioning
^^^^^^^^^^^^^^^^^^^^^^
+-------------------------------+---------------------------------------------------------------------------------------------------------------+
|          Name                 |                                                     Description                                               |
+===============================+===============================================================================================================+
|    Allow on-demand            | When enabled, a new view is added to the administration security settings, allowing you to fetch the LDAP     |
|    provisioning               | users before provisioning/syncing them. Provisioning users is also possible via the Public API. Note that     |
|                               | on-demand provisioning is only available for admin users.                                                     |
+-------------------------------+---------------------------------------------------------------------------------------------------------------+
|    All users filter           | This is the LDAP query used by DSS to fetch all the LDAP users used by the external users DSS UI view.        |
+-------------------------------+---------------------------------------------------------------------------------------------------------------+
|    Username attribute         | This is the LDAP attribute used as the username for the newly provisioned user.                               |
+-------------------------------+---------------------------------------------------------------------------------------------------------------+
|    Login remapping rules      | The LDAP username attribute may require remapping before being used as a DSS username, such as user email.    |
|                               | These rules are defined as search-and-replace Java regular expressions. Use ``(...)`` to capture substrings   |
|                               | and ``$1``, ``$2``, etc., to insert the captured substrings in the output. The rules are applied in order,    |
|                               | with each rule operating on the output of the previous one.                                                   |
+-------------------------------+---------------------------------------------------------------------------------------------------------------+
|    All groups filter          | This is the LDAP query used by DSS to fetch all the LDAP groups used by the external users DSS UI view.       |
+-------------------------------+---------------------------------------------------------------------------------------------------------------+
|    Group membership attribute | This is the LDAP attribute of an LDAP group that contains the user membership information.                    |
+-------------------------------+---------------------------------------------------------------------------------------------------------------+
|    Group membership user      | This is the LDAP attribute of an LDAP user that is used as a reference for the "group membership attribute".  |
|    attribute                  | DSS uses both the "group membership attribute" and this attribute to map users to groups.                     |
+-------------------------------+---------------------------------------------------------------------------------------------------------------+


* Refer to :ref:`ldap.templates` for typical values of the above parameters in common setups.


.. note::
  In both cases, DSS users mapped to LDAP accounts can be added / edited / deleted using the user management dialog described
  in :ref:`ldap.users`. Note however that if the automatic import of users is enabled, deleting a DSS account does not prohibit
  a user to connect, as their account will be recreated on next login.


.. _ldap.templates:

LDAP directory configuration templates
--------------------------------------

The following tables show reference configuration templates for LDAP connection parameters in common setups.

Standard LDAP directory using RFC2307 schema
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------+---------------------------------------------------+
|         Parameter             |                       Value                       |
+===============================+===================================================+
|         User filter           | (&(objectClass=posixAccount)(uid={USERNAME}))     |
+-------------------------------+---------------------------------------------------+
|         Display name          | cn                                                |
+-------------------------------+---------------------------------------------------+
|         Email                 | mail                                              |
+-------------------------------+---------------------------------------------------+
|         Group filter          | (&(objectClass=posixGroup)(memberUid={USERNAME})) |
+-------------------------------+---------------------------------------------------+
|         Group name            | cn                                                |
+-------------------------------+---------------------------------------------------+
|         All users filter      | (objectClass=posixAccount)                        |
+-------------------------------+---------------------------------------------------+
|         Username attribute    | uid                                               |
+-------------------------------+---------------------------------------------------+
|         All groups filter     | (objectClass=posixGroup)                          |
+-------------------------------+---------------------------------------------------+
|  Group membership attribute   | memberUid                                         |
+-------------------------------+---------------------------------------------------+
|  Group membership             | UID                                               |
|  user attribute               |                                                   |
+-------------------------------+---------------------------------------------------+



Standard LDAP directory using RFC2307bis schema
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the most frequently encountered case when connecting to Unix-based LDAP directories:

+-------------------------------------+-------------------------------------------------------+
|               Parameter             |                          Value                        |
+=====================================+=======================================================+
|              User filter            | (&(objectClass=posixAccount)(uid={USERNAME}))         |
+-------------------------------------+-------------------------------------------------------+
|             Display name            |                          cn                           |
+-------------------------------------+-------------------------------------------------------+
|                Email                |                         mail                          |
+-------------------------------------+-------------------------------------------------------+
|             Group filter            | (&(objectClass=posixGroup)(member={USERDN}))          |
+-------------------------------------+-------------------------------------------------------+
|              Group name             |                          cn                           |
+-------------------------------------+-------------------------------------------------------+
|         All users filter            |            (objectClass=posixAccount)                 |
+-------------------------------------+-------------------------------------------------------+
|        Username attribute           |                          uid                          |
+-------------------------------------+-------------------------------------------------------+
|        All groups filter            |            (objectClass=posixGroup)                   |
+-------------------------------------+-------------------------------------------------------+
|     Group membership attribute      |                        member                         |
+-------------------------------------+-------------------------------------------------------+
|   Group membership user attribute   |                          DN                           |
+-------------------------------------+-------------------------------------------------------+


Microsoft Active Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------+--------------------------------------------------+
|              Parameter              |                      Value                       |
+=====================================+==================================================+
|             User filter             | (&(objectClass=user)(sAMAccountName={USERNAME})) |
+-------------------------------------+--------------------------------------------------+
|            Display name             |                  displayName                     |
+-------------------------------------+--------------------------------------------------+
|                Email                |                      mail                        |
+-------------------------------------+--------------------------------------------------+
|            Group filter             |   (&(objectClass=group)(member={USERDN}))        |
+-------------------------------------+--------------------------------------------------+
|             Group name              |                        cn                        |
+-------------------------------------+--------------------------------------------------+
|         All users filter            |         (objectClass=user)                       |
+-------------------------------------+--------------------------------------------------+
|       Username attribute            |                 sAMAccountName                   |
+-------------------------------------+--------------------------------------------------+
|       All groups filter             |         (objectClass=group)                      |
+-------------------------------------+--------------------------------------------------+
|  Group membership attribute         |                     member                       |
+-------------------------------------+--------------------------------------------------+
|  Group membership user attribute    |                      DN                          |
+-------------------------------------+--------------------------------------------------+


.. note::

  Starting with Windows 2003 SP2, Active Directory servers can also resolve nested group membership
  using the following query for the group filter:

    (&(objectClass=group)(member:1.2.840.113556.1.4.1941:={USERDN}))


RedHat Identity Management and FreeIPA servers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------------------------+------------------------------------------------+
|            Parameter                |                     Value                      |
+=====================================+================================================+
|           User filter               | (&(objectClass=posixAccount)(uid={USERNAME}))  |
+-------------------------------------+------------------------------------------------+
|          Display name               |               displayName                      |
+-------------------------------------+------------------------------------------------+
|              Email                  |                   mail                         |
+-------------------------------------+------------------------------------------------+
|          Group filter               | (&(objectClass=groupOfNames)(member={USERDN})) |
+-------------------------------------+------------------------------------------------+
|            Group name               |                     cn                         |
+-------------------------------------+------------------------------------------------+
|        All users filter             |         (objectClass=posixAccount)             |
+-------------------------------------+------------------------------------------------+
|        Username attribute           |                    uid                         |
+-------------------------------------+------------------------------------------------+
|        All groups filter            |         (objectClass=groupOfNames)             |
+-------------------------------------+------------------------------------------------+
|    Group membership attribute       |                   member                       |
+-------------------------------------+------------------------------------------------+
|   Group membership user attribute   |                     DN                         |
+-------------------------------------+------------------------------------------------+


.. note::

  These servers also expose a RFC2307bis-compatible view of the directory in the LDAP subtree rooted at "cn=accounts".


.. _ldap.ssl:

Using secure LDAP connections
-----------------------------

Except in configurations where you closely control the network path between DSS and the LDAP server
(or in configurations where DSS and the LDAP server are installed on the same host), it is highly recommended to use
secure connections to the LDAP server, to avoid clear-text passwords being exposed to potential network eavesdroppers.

Depending on your LDAP server, there are two possible ways to configure this:

* use the non-standard but widely available LDAPS protocol (LDAP over SSL) where the client connects to the server on a
  network port dedicated to secure connections (default port: 636).

  DSS uses this connection mode when you configure an URL with scheme ldaps://.

* use the "Start TLS" standard protocol extension, where the client connects to the server using a normal (clear-text) LDAP
  connection on the standard port (default port: 389) but negotiates the establishement of a secure SSL channel over this
  connection before sending sensitive data through it.

  DSS uses this connection mode when you configure an URL with scheme ldap:// and check the "Use TLS" checkbox.

In both cases, this secure connection is only established if the LDAP client (here: Data Science Studio) can validate the
identity of the LDAP server, to avoid sending sensitive user passwords to a rogue server. In particular, the Java
runtime system used by Data Science Studio must be configured to trust the certificate of the LDAP server.

If your LDAP server certificate has been signed by a well-known certificate authority such as Verisign, you have
nothing to do since the certificate authority's root certificate is already in the default truststore used by the Java
runtime. Otherwise, you will need to obtain the root certificate of the certificate authority which issued the certificate
of your LDAP server, and add it to the truststore of the Java runtime used by DSS, using one of the procedures documented at
:ref:`java.ssl.truststore`.


.. _ldap.users:

Managing users
--------------

When LDAP integration is enabled, the Data Science Studio account database contains both local users
and users imported from the LDAP directory.

You can manage both type of accounts using the "Users" management page, accessible from the "Administration" menu
(you must be logged to DSS with administrator privileges).

* When editing a LDAP-based user entry, the password fields are not available as the user password is only managed and stored by
  the LDAP server.

* A local user entry can only be a member of local groups. A LDAP-based user can be a member of local groups as well as LDAP-based groups,
  but only the local group membership list can be edited. The LDAP-based group membership list for a user is dynamically read from
  the LDAP directory on each login.

* You can create a LDAP-based user account before the user's first connection, or configure DSS to automatically create it
  on the user's first connection. In the latter case, the user account is created with "Display name" and "email" attributes taken from
  the directory entry, if the corresponding attribute is configured and exists, and with an empty local group membership list. These fields
  can be adjusted by a DSS administrator after automatic account creation if needed.

.. _ldap.groups:

Managing groups
---------------

When LDAP integration is enabled, the Data Science Studio account database contains both local DSS groups
and DSS groups mapped to groups in the LDAP directory.

You can manage both type of groups using the "Groups" management page, accessible from the "Administration" menu
(you must be logged to DSS with administrator privileges).

A LDAP-based DSS group is defined by specifying a list of LDAP group names. Upon login, a LDAP-based DSS user `u`
will be assigned to a LDAP-based DSS group `g` whenever the LDAP user account for `u` is a member of any of the LDAP groups underlying
`g` in the directory.

Both LDAP- and local-based DSS groups can convey DSS administrator privileges, and DSS projects access rights, to a LDAP-based DSS user account.

If the "automatic import user" option is enabled, you will be able the define user profile for any LDAP group . This profile will only be applied for newly imported user and if a user belongs to many groups with a profile assigned the highest profile will be applied.
