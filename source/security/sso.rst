Single Sign-On
###############

.. note::

  DSS SSO implementation is an Authenticator and a User Supplier. See :doc:`Authentication </security/authentication/index>` documentation for more details.


Single sign-on (SSO) refers to the ability for users to log in just one time with one set of credentials
to get access to all corporate apps, websites, and data for which they have permission. 

By setting up SSO in DSS, your users will be able to access DSS using their corporate credentials. 

SSO solves key problems for the business by providing:

 * Greater security and compliance.
 * Improved usability and user satisfaction.

Delegating the DSS authentication to your corporate identity provider using SSO
allows you to enable a stronger authentication journey to DSS, with multi-factor authentication (MFA) for example.
 

DSS supports the following SSO protocols:

 * OpenID Connect (OIDC)
 * SAML v2
 * SPNEGO / Kerberos

.. warning::

	We strongly advise using SAML or OIDC rather than SPNEGO / Kerberos. Setting up SPNEGO is fairly difficult and may interact with connecting to Secure Hadoop clusters.

.. contents::
	:local:


Users supplier
==============

In SSO mode, users don't need to enter their password. Instead, the SSO system provides the proof that the person performing the query is who she pretends to be, and DSS verifies this proof.

However, DSS needs to map this identity to one of its users. This concept in DSS is called user supplying.

Using SSO provisioning
----------------------

DSS is able to provision users from the identity returned during the SSO protocol. It is not necessary to configure additional user sources.

By default, your identity provider usually only includes basic user attributes into the identity returned to DSS.
If you want to map the user groups, you will need to contact the identity provider administrator to include the groups in the identity claims.

.. warning::

	SSO can act as a user supplier and therefore provision/synchronize users. Since those operations can only happen during the login phase, you will therefore not
	be able to trigger a user synchronization manually from the UI or the API on SSO users.

Using an other external user source
-----------------------------------

You may choose to associate SSO with an external user source, like LDAP or Azure AD. Users will be able to authentication with SSO and be provisioned/synchronized from the given external source.

It is also possible to enable SSO provisioning and still have other external user sources. In that scenario, :ref:`set the order number <supporting-multiple-authenticators-and-user-suppliers>` of SSO to be higher than the other sources (so a larger order number).

Using local users
-----------------

If you don't want to enable SSO provisioning or any other user suppliers like LDAP, you need to create DSS user accounts for the SSO users. When creating these users, select "SSO" as source type. 
This way, only a login and display name are required, you don't need to enter a password (since DSS delegates authentication in SSO mode).


OpenID Connect (OIDC)
========================

About OIDC
-----------------

.. |DKU_APP| replace:: DSS

.. include:: /security/sso/_oidc_about.txt

Setup OIDC in DSS
---------------------

.. include:: /security/sso/_oidc_setup.txt


SAML
====

When configured for SAML single-sign-on, DSS acts as a SAML Service Provider (SP), which delegates user authentication
to a SAML Identity Provider (IdP).

About SAML
-----------------

.. include:: /security/sso/_saml_about.txt


Setup SAML in DSS
---------------------

.. |SAML_CALLBACK_PATH| replace:: BASE_URL/dip/api/saml-callback
.. |SAML_CALLBACK_URL_EXAMPLE| replace:: https://dss.mycompany.corp
.. |SAML_CALLBACK_PATH_EXAMPLE| replace:: https://dss.mycompany.corp/dip/api/saml-callback

.. include:: /security/sso/_saml_setup.txt


Troubleshooting
-----------------

No details are printed in case of wrong SSO configuration. All details are only in the logs.

Common issues include:

Assertion audience does not include issuer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This means that the EntityID declared in the DSS SP configuration does not match the expected EntityID / audience at the IdP level.

Response is destined for a different endpoint
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check the "ACS URL" in the DSS SP configuration. It must match the response destination in the IdP answer, ie generally the callback
declared in the IdP.

This error message also shows up when the IdP does not include a "Destination" attribute in the response message. This attribute
is mandatory and should match the DSS SAML callback URL.

When using PingFederate PingIdentity as an IdP make sure to **uncheck** the *Always Sign the SAML Assertion* property when
defining the DSS endpoint, to ensure that a Destination attribute is included in the Response message.

DSS would not start after configuring SAML SSO
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some cases (in particular, entering invalid XML in the IdP Metadata field), an incorrect SAML configuration may 
prevent the DSS backend to start. In such a case, open the ``DSS_DATADIR/config/general-settings.json`` configuration file
with a text editor, locate the ``"enabled"`` field under ``"ssoSettings"`` and set it to ``false``.
You should then be able to restart and fix the configuration using the DSS interface.

Login fails with "Unknown user <SOME_STRING>"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This typically means that SAML authentication of the user was successful at the IdP level, but that the returned attribute
does not match any username in the DSS database (or in the associated LDAP directory if one has been configured).

It might be because you did not select the correct SAML attribute name in the DSS SAML configuration. You can check the list of
attributes returned by the IdP in the DSS backend log file.

It might be because the attribute rewrite rule(s) did not lead to the expected result. This can also be checked in the DSS backend
log file.

It might be because no DSS user exists with this name. You can create one in the DSS "Security / Users" page, using type
"Local (no auth, for SSO only)".

No acceptable Single Sign-on Service found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

DSS only supports the HTTP-Redirect binding for SAML requests, and requires one such binding to be defined.
If configured with an IdP metadata record which does not contain such a binding, the DSS backend will fail to start and output a
``SAMLException: No acceptable Single Sign-on Service found`` message in the backend log file.

To fix that, you need to edit the IdP Metadata record and add a ``SingleSignOnService`` XML node inside the ``IDPSSODescriptor`` node, as follows:

.. code-block:: none

    <md:EntityDescriptor ...>
        <md:IDPSSODescriptor ...>
    	    ...
            <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="SOME_VALID_REDIRECT_URL"/>
        </md:IDPSSODescriptor>
    </md:EntityDescriptor>

This entry defines the URL to which DSS will redirect users which attempt to connect without a currently valid authentication cookie.
Any valid URL can be configured in it, you can for example use the address to the login page for your IdP.

Note that this address will never be used if users only connect to DSS through IdP-initiated SAML connections. It is nevertheless mandatory to configure one.


SPNEGO / Kerberos
==================

.. warning::

	While this is somewhat related to Kerberos securitization of secure Hadoop clusters, these are two very different
	and independent features

.. warning::

	We strongly advise using SAML SSO rather than SPNEGO / Kerberos. Setting up SPNEGO is fairly difficult, requires specific
	configuration of the user browsers, and may interact with connecting to Secure Hadoop clusters.


Keytab mode
------------

The recommended way to setup SPNEGO authentication is to create a service principal for DSS in your Kerberos database, along
with an associated keytab file. This keytab allows DSS to authenticate the users identity through the Kerberos login session
of their browser.

The principal and keytab will be provided by your Kerberos administrator. The keytab file must be installed on the DSS machine,
in a filesystem location readable by, and private to, the DSS Unix service account.

You may also have to provide a krb5.conf file if the server does not have a suitable one in the default system location. This file
will also be provided by your Kerberos administrator.

.. note::

	The Kerberos principal used by DSS for SPNEGO authentication MUST be of the form ``HTTP/<dss_hostname>@<realm>``
	where <dss_hostname> is the hostname of the DSS service URL as seen from the client's browser.

	On Windows Active Directory, service principals are created by:

	* creating a user account for DSS in the domain
	* associating the required service principal to this account, using the command-line 'setspn' tool (you can also
	  do it using extra arguments to the 'ktpass' command which issues the Kerberos keytab file).


Custom JAAS mode
-----------------

For advanced use cases not covered by the previous mode. Requires advanced knowledge of Kerberos configuration for Java.


Login remapping rules
---------------------

Optionally, you can define one or several rewriting rules to transform the user identity provided by SPNEGO (which is the 
Kerberos principal of the user, typically username@REALM) into the intended DSS username.

These rules are standard search-and-replace Java regular expressions, where ``(...)`` can be used to capture a substring in the 
input, and ``$1``, ``$2``... mark the place where to insert these captured substrings in the output. Rules are evaluated in 
order, until a match is found. Only the first matching rule is taken into account.

For convenience, a standard rule which strips the @REALM part of the user principal can be enabled by a checkbox in the configuration.
This rule is evaluated first, before any regular expression rules.


Configuring SPNEGO SSO
-------------------------

* Go to Administration > Settings > LDAP & SSO
* Enable the SSO checkbox, select SPNEGO, and enter the required information
* Restart DSS
* Access the DSS URL
* If login fails, check the logs for more information

.. note::

	Once SSO has been enabled, if you access the root DSS URL, SSO login will be attempted. If SSO login fails, you will only see an error.

	You can still use the regular login/password login by going to the ``/login/`` URL on DSS. This allows you to log in if SSO login is dysfunctional

.. note::
	
	You will typically need to perform additional configuration on the user browsers so that they attempt SPNEGO authentication
	with DSS. This usually includes:

	* making sure the user session is logged on the Kerberos realm (or Windows domain) before launching the browser
	* adding the DSS URL to the list of URLs with which the browser is authorized to authenticate using Kerberos

	Refer to your browser documentation and your domain administrator for the configuration procedures suitable for your site.


Troubleshooting
-----------------

No details are printed in case of wrong SSO configuration. All details are only in the logs.

SPNEGO failures are notoriously hard to debug because all communication is encrypted, and any error simply leads to decryption failures.

Usual things to double-check:

* The mapping of ``domain_realm`` in your krb5.conf
* The principal in the keytab must match the one declared in DSS
* The principal in the keytab must be HTTP/<dss_hostname>@<realm> where <dss_hostname> matches the DSS URL hostname.
* The browser must be configured to allow SPNEGO authentication on <dss_hostname>. In particular, error messages mentioning
  NTLM authentication failures actually mean that this configuration is not working as expected.
