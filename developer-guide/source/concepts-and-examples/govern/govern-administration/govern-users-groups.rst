Users and groups
#################

The API exposes key parts of the Dataiku Govern access control management: users and groups. All these can be created, modified and deleted through the API.


Example use cases
=================

In all examples, `client` is a :class:`dataikuapi.govern_client.GovernClient`, obtained using :meth:`dataikuapi.govern_client.GovernClient.__init__`


Listing users
--------------

.. code-block:: python

	client = GovernClient(host, apiKey)
	govern_users = client.list_users()
	# govern_users is a list of dict. Each item represents one user
	prettyprinter.pprint(govern_users)

outputs

::

	[   {   'displayName': 'Administrator',
	        'groups': ['administrators', 'data_scientists'],
	        'login': 'admin',
	        'sourceType': 'LOCAL'},
	    ...
	]

Creating a user
----------------

A local user with a password
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.. code-block:: python
	
	new_user = client.create_user('test_login', 'test_password', display_name='a test user', groups=['all_powerful_group'])

new_user is a :class:`dataikuapi.govern.admin.GovernUser`

A user who will login through LDAP
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Note that it is not usually required to manually create users who will login through LDAP as they can be automatically provisionned

.. code-block:: python
	
	new_user = client.create_user('test_login', password=None, display_name='a test user', source_type="LDAP", groups=['all_powerful_group'], profile="DESIGNER")

A user who will login through SSO
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

This is only for non-LDAP users that thus will not be automatically provisioned, buut should still be able to log in through SSO.

.. code-block:: python
	
	new_user = client.create_user('test_login', password=None, display_name='a test user', source_type="LOCAL_NO_AUTH", groups=['all_powerful_group'], profile="DESIGNER")

Modifying a user's display name, groups, profile, email, ...
-------------------------------------------------------------

To modify the settings of a user, get a handle through :meth:`dataikuapi.govern_client.GovernClient.get_user`, then use :meth:`dataikuapi.govern.admin.GovernUser.get_settings`

.. code-block:: python

	user = client.get_user("theuserslogin")

	settings = user.get_settings()

	# Modify the settings in the `get_raw()` dict
	settings.get_raw()["displayName"] = "Govern Lover"
	settings.get_raw()["email"] = "my.new.email@stuff.com"
	settings.get_raw()["userProfile"] = "DESIGNER"
	settings.get_raw()["groups"] = ["group1", "group2", "group3"] # This completely overrides previous groups

	# Save the modifications
	settings.save()

Deleting a user
----------------

.. code-block:: python
	
	user = client.get_user('test_login')
	user.delete()

Impersonating another user
---------------------------

As a Dataiku Govern administrator, it can be useful to be able to perform API calls on behalf of another user.

.. code-block:: python

    user = client.get_user("the_user_to_impersonate")
    client_as_user = user.get_client_as()

    # All calls done using `client_as_user` will appear as being performed by `the_user_to_impersonate` and will inherit
    # its permissions

Listing groups
----------------

A list of the groups can by obtained with the `list_groups` method:

.. code-block:: python

	client = GovernClient(host, apiKey)
	# govern_groups is a list of dict. Each group contains at least a "name" attribute
	govern_groups = client.list_groups()
	prettyprinter.pprint(govern_groups)

outputs

::

	[   {   'admin': True,
	        'description': 'Govern administrators',
	        'name': 'administrators',
	        'sourceType': 'LOCAL'},
	    {   'admin': False,
	        'description': 'Read-write access',
	        'name': 'data_scientists',
	        'sourceType': 'LOCAL'},
	    {   'admin': False,
	        'description': 'Read-only access',
	        'name': 'readers',
	        'sourceType': 'LOCAL'}]


Creating a group
-----------------

.. code-block:: python
	
	new_group = client.create_group('test_group', description='test group', source_type='LOCAL')

Modifying settings of a group
------------------------------


First, retrieve the group definition with a `get_definition` call, alter the definition, and set it back into Govern:

.. code-block:: python

	group_definition = new_group.get_definition()
	group_definition['admin'] = True
	group_definition['ldapGroupNames'] = ['group1', 'group2']
	new_group.set_definition(group_definition)

Deleting a group
------------------

.. code-block:: python
	
	group = client.get_group('test_group')
	group.delete()

Reference documentation
=======================

.. autosummary:: 
	dataikuapi.govern.admin.GovernUser
	dataikuapi.govern.admin.GovernUserSettings
	dataikuapi.govern.admin.GovernOwnUser
	dataikuapi.govern.admin.GovernOwnUserSettings
	dataikuapi.govern.admin.GovernGroup