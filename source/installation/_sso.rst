Single Sign-On
###############

Single sign-on (SSO) refers to the ability for users to log in just one time with one set of credentials
to get access to all corporate apps, websites, and data for which they have permission. 

By setting up SSO in FM, your users will be able to access FM using their corporate credentials. 

SSO solves key problems for the business by providing:

 * Greater security and compliance.
 * Improved usability and user satisfaction.

Delegating the FM authentication to your corporate identity provider using SSO
allows you to enable a stronger authentication journey to FM, with multi-factor authentication (MFA) for example.
 
FM supports the following SSO protocols:

 * OpenID connect
 * SAML


Users database
==============

Since FM users all have the same privileges, we recommend that you simply map all your login users to the admin user.

If you choose not to map to the same user, you must create FM user accounts for each SSO user. When creating these users, select "Local (no auth, for SSO only)" as the source type.
Since users won't enter passwords in SSO mode, only a login and display name are required.



OpenID Connect
========================

About OIDC
-----------------

.. |DKU_APP| replace:: FM

.. include:: /security/sso/_oidc_about.txt


Setup OIDC in FM
---------------------

.. include:: /security/sso/_oidc_setup.txt


SAML
====

About SAML
-----------------


.. include:: /security/sso/_saml_about.txt


Setup SAML in FM
---------------------

.. |SAML_CALLBACK_PATH| replace:: BASE_URL/api/saml-callback
.. |SAML_CALLBACK_URL_EXAMPLE| replace:: https://fm.mycompany.corp
.. |SAML_CALLBACK_PATH_EXAMPLE| replace:: https://fm.mycompany.corp/api/saml-callback

.. include:: /security/sso/_saml_setup.txt

