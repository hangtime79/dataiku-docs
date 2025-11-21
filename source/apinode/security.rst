Security
#########

.. contents::
	:local:

Security for API Node administration API
=========================================

The API node administration API can only be queried through administrative API keys.

API node administrative API keys are managed by the ``./bin/apinode-admin`` tool (see :doc:`operations/cli-tool` for more information).

.. code-block:: bash

	./bin/apinode-admin admin-key-create
	./bin/apinode-admin admin-keys-list
	./bin/apinode-admin admin-key-delete KEY

Each API key has full administrative permissions; the API node does not have fine-grained administrative privileges.

Permissions for API Deployer
==============================

The API deployer offers per-group permissions on Published API Services and Infrastructures.

There are no permissions on the deployments:

* You may read details of a deployment if you have "read" permission on both the service and the infrastructure
* You may create a new deployment if you have "deploy" permission on both the service and the infrastructure

This gives a large amount of flexibility for implementing:

* A system where some API services are "public" while some are restricted even from viewing
* A system where data scientists may deploy any API service to development and testing infrastructures, but only a small set of devops may deploy to the production infrastructure

Infrastructures
----------------

Infrastructures may only be initially created by global DSS administrators.

Once an infrastructure is created, an arbitrary number of groups may be granted access with the following privileges:

* View: view this infrastructure, view associated deployments (if you also have Read permission on the service)
* Deploy: use this infrastructure to create deployments, update, enable/disable deployments on this infrastructure, manage their settings (if you also have Deploy permission on the service)
* Admin: manage infrastructure settings, including managing permissions

To manage infrastructure privileges, go to API Deployer > Infrastructure > Settings > Permissions.

Services
---------

Services may be created by any user who has the global "Create API Service" privilege (this is handled at the Group level, see :doc:`/security/permissions`).

The user who creates the service is automatically assigned as "Owner" of the service, which grants full access to the service.

The owner, or any group who has "Admin" privilege on the service, can grant access to an arbitrary number of groups with the following privileges:

* Read: view this service, view associated deployments (if you also have Read permission on the infrastructure) - Note that this gives the ability to see API keys for the service
* Write: manage versions of this service (upload, delete)
* Deploy: create new deployments of this service, update, enable/disable deployments of this service, manage their settings (if you also have Deploy permission on the infrastructure)
* Admin: manage service settings, including managing permissions and deleting service

To manage service privileges, go to API Deployer > API Services > Settings > Permissions.

Authorization
=============

To protect access to your services deployed on an API node, DSS supports the following authorization methods:

* Public: (default) No authorization is required to access the service.
* API keys: Create a set of static API keys, which you can use to access the service afterwards.
* JWT/OAuth2: Configure the API node to accept Json Web Token (JWT) from a trusted third party. Additionally, if the third party is an OAuth2 provider, the API node can be configured to verify the JWT as an access token as specified in the OAuth2 specification.

API Keys
---------

An API key is a token that clients must provide when making API calls. You must first define a set of static keys in DSS that are specific to the API.
The API node will ensure that only requests using one of these keys are allowed to access the service.

With this method, DSS manages the keys and therefore takes care of the access management. This method is preferable if your organization does not yet have an IAM.

The API keys authorization method offers the following characteristics:

* You can create an arbitrary number of API keys
* API keys are per API Service
* Each API key has full access to the API service (there is no per-endpoint security)
* Using multiple API keys gives traceability and the ability to revoke a compromised API key
* No need of an IAM

JWT/OAuth2
-----------

The API node supports authorizing requests accesses using a Json Web Token (JWT).
When this JWT is actually an access token issued by an OAuth2 provider, the API node will do some additional security checks, like scopes.

.. note:: There is no enforcement of using OAuth2 when using this authorization method. If you have an internal system that issues JWTs, you can configure the API node to accept those JWTs using this authorization method.

Using this authorization method, DSS delegates access management to a third party, usually an IAM.
Instead of managing access, as with API keys, DSS will only establish a trust relationship with the IAM.
It will be the responsibility of the IAM to ensure that the JWTs issued contain the correct permissions.
The API node will only verify that the tokens are issued by the IAM and that the claims contained in the tokens are valid for the current service.

This method is preferred if your organization has an IAM in place and/or if you want to manage API access outside of DSS.

The JWT/OAuth2 authorization method offers the following characteristics:

* DSS delegates access management to a third party
* You can easily revoke access directly in the third party and this will be reflected in DSS without any manual intervention
* You can align the authorization method across all your organization APIs
* OAuth2 is a well-known standard which your API consumers will most likely be used to
* JWT allows you to leverage strong cryptography, with options like keys rotation.


Without API Deployer
=====================

When not using API Deployer, security is configured at design time, in the DSS Design node:

* From the Service page, go to the `Security > Authorization` tab
* Select the authorization method of your choice.

When you create the package, the authorization settings are packaged with it, and when you activate the deployment in the API Nodes, they are propagated.

With API Deployer
==================

When using API Deployer, in addition to the method mentioned above (defining the authorization method at design time), you can also set security on a per-deployment basis.

This allows you to have different authorization method settings, like different API keys, for development and production deployments of the same API Service.

* Go to `Deployment > Settings > Authorization`
* Select whether you want to use the security settings defined in the API Designer, or override them for this deployment

When choosing the authorization method `API keys`, the API Deployer screen and sample code will show the first API Key, but all API keys will work similarly.

Your POST requests will now require an additional `user` parameter. For example, it will look something like:

.. code-block:: bash

	curl -X POST --header 'Authorization: Bearer 1234APIKEY56789' \
  	URL \
  	--data '{
    	"key": "value"
  	}'

How to setup JWT/OAuth2 authorization method
=============================================

.. note:: Whether you choose to setup this method in the design node or at the deployer level, the JWT/OAuth2 setting works the same way.

This authorization method delegates the access management to a third party by relying on signed tokens (JWS) to access the API.
The JWT settings will allow DSS to only trust JWTs issued by this third party.

Keys format
-----------

The API node only accepts digitally signed JWTs. In order to verify these signed JWTs (JWS), DSS needs to verify the
signature. Currently, DSS only support signing using asymmetric keys, meaning DSS will need to obtain the public keys used to sign the JWTs.

DSS is expecting the public keys to be in a JWKs set format, as per the `RFC 7517 <https://datatracker.ietf.org/doc/html/rfc7517#section-5>`_.
The following methods supported to retrieve the public keys:

* `JWKs_URI`: provide the public keys in a JWKs set format, behind a URI.
* `static JWKs set`: provide some static public keys in a JWKs set format.

Using a JWKs_URI is recommended, it has the advantage of allowing you to:

* rotate the keys without any manual configuration changes needed in DSS
* delegate the management of those keys to your third party
* have a large set of keys
* use the out of the box JWKs_URI from your IAM, a feature supported by most modern IAMs.

.. note::

	The supported signing algorithms are:

	* RSA
	* Elliptic Curve

Issuer
------

Inside the JWT is defined the `iss` (issuer) claim which identifies the principal that issued the JWT.
By only trusting JWTs with a specific `iss` value, it ensures that the API node only accept tokens issued by this principal.

If you are using an IAM, you may not be aware of which `iss` it uses. Please contact your IAM admin system to retrieve the issuer.
Although, in some case, you can discover this value by:

* Create an access token and introspect the claims using `jwt.io <https://jwt.io>`_ . You will be able to retrieve the issuer value from the `iss` claim.
* The IAM may offer a discovery endpoint, which contains the `issuer` value, as per the `OIDC discovery specification <https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderMetadata>`_. The issuer will be part of the response.

Audience
---------

.. note:: In most OAuth2 setups, you can leave it blank, as access tokens are not bound to a specific resource server (unless your organization is enforcing `RFC 8707 <https://datatracker.ietf.org/doc/html/rfc8707>`_).

You can choose to define the audience if you know that all the JWTs will always have the same `aud`.
This is the case if the JWTs are dedicated to this API and you want to make sure tokens intended for other APIs are rejected.

Scope
---------

.. note:: This setting is optional

It is recommended to configure the `scope` when using OAuth2.
Scopes in OAuth2 allow you to perform granular permission checks on your API.
If setup, the API node will verify the token contains the specified scope.

This is particularly handy if you got multiple APIs, with dedicated scopes for each of them, and you want to make sure only users or applications with the
right privileges are allowed accesses to your API.

Scope claim key
----------------

.. note:: Only required if you defined a scope.

When scope validation is enabled, the API node needs to know which claim contains the scopes.
This claim is usually `scope`, but there is no standard. This setting allows you to override the claim key.

Scope claim format
-------------------

.. note:: Only required if you defined a scope.

When scope validation is enabled, the API node needs to know the format of the scope claim.
The standard convention in OAuth2 is to have the `scope` as a `string`, although this is not enforced. Optionally, DSS also supports the `array` format for compatibility with IAMs which don't yet respect the OAuth2 convention.

Client ID claim Key
-------------------

The access token is issued for an application, referred to as the OAuth2 Client.
For audit reason (see :doc:`../operations/audit-trail/apinode` for more information), you may want to know the OAuth2 client behind a request.
The Client ID is usually in a dedicated claim `client_id`, although this isn't standardized. This setting allows the API node to retrieve the client ID from a specified claim, whose format is expected to be `string`
retrieve the client ID from the token. The format of this claim is expected to be a `String`.


Send requests to an API protected with JWT/OAuth2
=================================================

Once you have setup the JWT/OAuth2 authorization method, you will need to retrieve a token from the third party.

The token must then be sent to the API node using the `Authorization` header, as follow:

.. code::

	Authorization: Bearer <token>

Using OAuth2
--------------

You may have chosen to configure the JWT/OAuth2 settings for an OAuth2 provider.
In this scenario, the JWT token is an access token and the API node acts as a resource server.
The API node is agnostic about how you retrieve the access token from the OAuth2 provider.
It will only check the validity of the token. Therefore you can choose to retrieve the access token using the authorization grant of your choice (see `RFC 6749 <https://datatracker.ietf.org/doc/html/rfc6749#section-1.3>`_ for more information).
If you are unsure, please contact your IAM admin for more details on which grant you should use and how.

Once you have retrieved an access token, it can be sent to the API node using the same `Authorization` header:

.. code::

	Authorization: Bearer <access-token>
