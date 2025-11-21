User secrets
#############

There are various cases in which you may want to use, in code recipes, credentials that are specific to a user.

For example:

* A code recipe or plugin dataset connecting to an external API to fetch data
* A code recipe or custom exporter that sends data to an external service for custom exports

DSS offers a mechanism for users to enter their credentials in their profile. DSS then encrypts the credentials, and code running under the identity of a given user can then retrieve the decrypted version of the credentials.

User secrets are kept encrypted at rest. See :doc:`passwords-security` for more information.

User secrets are personal and cannot be shared. DSS does not have a concept of "global secrets".

Entering user secrets
======================

* Go to your profile page
* Go to the "My Account" tab
* In the "Other credentials", click "Add"

Each user secret has a Name, and a value. The name is an identifier that must be used by the code that wants to retrieve the secret, in order to identify it. The value is the secret itself.

Click "Ok", then click "Save". Your secret is now stored by DSS

Using user secrets
===================

User secrets can be used in Python or R code

Python
------

This can be used in any Python code that runs under the identity of a user:

* A recipe
* A notebook
* A plugin recipe
* An external public API user using a personal API key
* ...

See :doc:`devguide:api-reference/python/index` for more information on using API clients

.. code-block:: python

	# client is a dataikuapi.DSSClient

	auth_info = client.get_auth_info(with_secrets=True)

	# retrieve the secret named "credential-for-my-api"
	secret_value = None
	for secret in auth_info["secrets"]:
		if secret["key"] == "credential-for-my-api":
			secret_value = secret["value"]
			break

	if not secret_value:
		raise Exception("secret not found")

	# Use secret_value

R
-

This can be used in any R code that runs under the identity of a user:

* A recipe
* A notebook
* A plugin recipe

.. code-block:: R

	library(dataiku)

	auth_info = dkuGetAuthInfo(with_secrets = TRUE)

	# Find the correct secret
	secret <- auth_info$secrets[lapply(auth_info$secrets, function(d) { d$key == "credential-for-my-api"}) == TRUE] 
	secret_value <- secret[[1]]$value

	# Use secret_value


