Authentication information and impersonation
##############################################

Introduction
=============

From any Python code, it is possible to retrieve information about the user or API key currently running this code.

This can be used:

* From code running outside of Dataiku Govern, simply to retrieve details of the current API key

Furthermore, the API provides the ability, from a set of HTTP headers, to identify the user represented by these headers.


Code samples
=============

Getting your own login information
------------------------------------

.. code-block:: python

     auth_info = client.get_auth_info()

     # auth_info is a dict which contains at least a "authIdentifier" field, which is the login for a user
     print("User running this code is %s" % auth_info["authIdentifier"])

Impersonating another user
---------------------------

As a Dataiku Govern administrator, it can be useful to be able to perform API calls on behalf of another user.

.. code-block:: python

    user = client.get_user("the_user_to_impersonate")
    client_as_user = user.get_client_as()

    # All calls done using `client_as_user` will appear as being performed by `the_user_to_impersonate` and will inherit
    # its permissions


Reference documentation
==========================

.. autosummary:: dataikuapi.govern_client.GovernClient.get_auth_info
