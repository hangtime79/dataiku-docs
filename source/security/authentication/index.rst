Authentication
##############

.. toctree::
   :maxdepth: 2

   multifactor-authentication
   ldap
   ../sso
   azure-ad
   custom

This section provides an overview of Identity Access Management (IAM) concepts in Dataiku DSS.

Authentication and user provisioning
====================================

In Dataiku DSS, authentication and user provisioning are two separate processes.

Authentication is the process of verifying a user's identity and granting access to the system. It involves validating username/password credentials and returning the user's identity.

User provisioning, on the other hand, is the process of retrieving a user matching this identity from an external source (LDAP, Azure AD, a custom database...) and creating or synchronizing the corresponding user in DSS. It ensures that the user's information and access privileges are correctly mapped within the system.

For example, you can enforce users to log in with Single Sign-On (SSO) while synchronizing their user data from an LDAP server. In this scenario, SSO serves as the authenticator, and LDAP acts as the user supplier.

User synchronization is the process of applying changes that happened on the identity of the user in the external source, to the matching user in DSS.

User synchronization and provisioning can happen automatically at login time, or on-demand by an admin either through the user interface or the public API.

Supported authenticators and user suppliers
===========================================

Dataiku DSS supports the following authenticators and user suppliers. If the authenticator or user supplier you require is not listed, you can submit a feature request or contribute a :doc:`custom authenticator/user supplier through a plugin <custom>`.

Authenticators
--------------

- `Local`: Allows users to log in using username/password credentials stored directly in DSS.
- `SSO`: Delegates authentication to an identity manager using the `SAML` or `OpenID Connect` protocols.
- `LDAP`: Enables users to log in using username/password credentials stored in an LDAP server.
- `PAM`: Enables users to log in using username/password credentials via PAM (Pluggable Authentication Modules).
- `Custom`: Provides the flexibility to create a custom authenticator to authenticate users using username/password credentials.

User suppliers
--------------

- `SSO`: The chosen SSO protocol returns an identity (ID token, SAML assertion, etc.) from the SSO authenticator which is used to provision or synchronize the user in DSS during login.
- `LDAP`: Fetches the user information from the LDAP server and provisions/synchronizes it as a DSS user.
- `Azure AD`: Fetches the user information from Azure AD and provisions/synchronizes it as a DSS user.
- `PAM`: Limited functionality; PAM can only provision/synchronize a user with the username information, and only for users authenticated using PAM.
- `Custom`: Allows the creation of a custom user supplier to convert the identity obtained during authentication into a DSS user.


.. _mapping-profiles-and-groups:

Mapping profiles and groups
===========================

When a user is provisioned or synchronized to DSS, their profile is determined based on the "User profiles" settings of the user supplier it originates from.

.. image:: img/profile-mappings.png

- You can define a mapping for each group in your external source to a corresponding Dataiku DSS profile.
- A default user profile must be defined.

The user profile is determined as follows: for each external group the user belongs to, DSS retrieves the corresponding profile mapping (if any) as well as the default profile.
The user is assigned the profile that is listed first in the license, typically corresponds to the profile with the highest privileges.

Similarly, a user can be automatically added to DSS groups using group mappings. Group mappings are configured in DSS under "Administration" > "Security" > "Groups".

.. image:: img/group-mappings.png

The "Type" specifies the source of the external group, and the list of groups (e.g. LDAP groups) is a list of external groups.
If a user belongs to an external group that has a group mapping, they will be automatically added to the corresponding DSS group.

.. _synchronizing-user-attributes:

Synchronizing user attributes
=============================

User attribute synchronization can be enabled during login and as an on-demand option through the user interface.

.. image:: img/allow-user-synchronization.png

To manually synchronize all external users, navigate to the users management screen (`Administration` > `Security` > `Users`) and click the `SYNC ALL` button.

To synchronize a specific user, go to their user profile page and click the `SYNC` button next to their `Type`.

.. note::

  Only user suppliers capable of fetching a user from its identity support on-demand synchronization. For example, the SSO supplier does not allow manual synchronization and only synchronizes users during login.

You can choose which user attributes to synchronize by configuring the following settings:

.. image:: img/attribute-synchronization-settings.png

In this section, you can also choose which action should be triggered when a user is either not present in the external source or not in the authorized groups anymore.
`Add a warning in the logs` will stop the user from authenticating but won't affect any existing API key that the user may have created.
On the contrary, `Disable user in DSS` will alter the user and make sure all the associated API keys won't pass the authorization phase anymore.

Advanced functionalities
========================

.. _supporting-multiple-authenticators-and-user-suppliers:

Supporting multiple authenticators and user suppliers
-----------------------------------------------------

Dataiku DSS offers the flexibility to configure multiple authenticators and user suppliers, allowing you to accommodate users from different user stores. When setting up multiple sources, the order of authenticators and user suppliers becomes significant, especially when a user exists in multiple sources.

To manage the order of authenticators and user suppliers, you can configure the security settings in the `general-settings.json` file. By default, the order in DSS is as follows: `Local` > `LDAP` > `Azure AD` > `SSO` > `PAM` > `Custom`.

When a user attempts to connect to DSS for the first time, they need to be provisioned. DSS goes through the authenticators and user suppliers in the specified order and creates a DSS user associated with the appropriate source.

.. warning::

	Once a DSS user is associated with a given source, DSS will only try this source to synchronize the user. Changing the source is manual.

Example scenarios
-----------------

Let's consider a setup with the following configurations:

Setup:

- Single Sign-On (SSO) is configured using the OpenID protocol with Google as the identity provider.
- SSO provisioning is enabled.
- LDAP is configured, and LDAP authentication is enabled.
- Azure AD is configured as well.
- The LDAP server contains a user named `alice`.
- The Azure AD server contains a user named `bob`.
- There is a user named `charlie` with a Google account, but this user is not present in LDAP or Azure AD.

Situation 1: Alice connects to DSS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Alice connects using SSO.
- DSS trusts the identity provided by SSO.
- As DSS does not find a user named `alice` among its local users, it triggers the provisioning process.
- DSS proceeds with the user suppliers, starting with LDAP (following the order specified).
- LDAP successfully retrieves a user named `alice`.
- DSS creates a DSS user named `alice` with the `LDAP` source type.

From this point on, Alice can connect to DSS either with SSO or LDAP since LDAP authentication is enabled. If you want to enforce Alice to use SSO exclusively, you can disable authentication for LDAP. DSS will synchronize Alice's user with LDAP during each login and will not attempt to synchronize with Azure AD, even if Alice exists in Azure AD.

Situation 2: Bob connects to DSS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Bob connects using SSO.
- DSS trusts the identity provided by SSO.
- As DSS does not find a user named `bob`, it triggers the provisioning process.
- DSS proceeds with the user suppliers, starting with LDAP (following the order specified).
- LDAP does not find a user named `bob`.
- DSS moves on to the next user supplier, which is Azure AD.
- Azure AD successfully retrieves a user named `bob`.
- DSS creates a DSS user named `bob` with the `AZURE_AD` source type.

As the DSS implementation for Azure AD only supports user supplying, Bob can only connect to DSS using SSO.
 
Situation 3: Charlie connects to DSS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Charlie connects using SSO.
- DSS trusts the identity provided by SSO.
- As DSS does not find a user named `charlie`, it triggers the provisioning process.
- DSS proceeds with the user suppliers, starting with LDAP (following the order specified).
- LDAP does not find a user named `charlie`.
- DSS moves on to the next user supplier, which is Azure AD.
- Azure AD does not find a user named `charlie`.
- DSS moves on to the next user supplier, which is SSO.
- SSO successfully returns a user named `charlie` using the identity returned during the SSO protocol.
- DSS creates a DSS user named `charlie` with the `SSO` source type.

From now on, Charlie can only connect with SSO. Even if a user named `charlie` is created in Azure AD, DSS will not attempt to synchronize with Azure AD.
To synchronize `charlie` with Azure AD, you would need to manually change the source type of the DSS user `charlie` to Azure AD.