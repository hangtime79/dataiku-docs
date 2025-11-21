Data Collections
################

..
  this code samples has been verified on DSS: 14.1.0
  Date of check: 10/09/2025
    create_data_collection does not work anymore -- team navi is aware of.

  this code samples has been verified on DSS: 13.2.0
  Date of check: 04/10/2024

You can interact with the Data Collections through the API.

Basic operations
================

Listing Data Collections
------------------------

.. code:: python

	data_collections = client.list_data_collections(as_type="objects")
	# Returns a list of DSSDataCollection

	for data_collection in data_collections:
		settings = data_collection.get_settings()

		# Access to main information in the Data Collection
		print("Data Collection id: %s" % settings.id)
		print("Display name: %s" % settings.display_name)
		print("Description: %s" % settings.description)
		print("Color: %s" % settings.color)
		print("Tags: %s" % settings.tags)
		print("Permissions: %s" % settings.permissions)

		# You can also list the objects in a Data Collection
		print("Content: %s" % data_collection.list_objects(as_type='dict'))

Modifying Data Collection
-------------------------

.. code-block:: python

	data_collection = client.get_data_collection("someDcId")
	settings = data_collection.get_settings()
	settings.display_name = "new name"
	settings.permissions = [*settings.permissions, DSSDataCollectionPermissionItem.reader_user("LOGIN"), DSSDataCollectionPermissionItem.contributor_group("GROUP")]
	settings.save()

Creating a Data Collection
--------------------------

.. code-block:: python

	data_collection = client.create_data_collection("The name of the collection", description="Description *markdown is allowed*")
	# returns a DSSDataCollection that can be used for adding objects

Deleting a Data Collection
--------------------------

.. code-block:: python

	data_collection = client.get_data_collection("someDcId")
	data_collection.delete()

Adding and deleting the objects in a Data Collection
====================================================

.. code-block:: python

	data_collection = client.get_data_collection("someDcId")
	data_collection_objects = data_collection.list_objects()

	# remove all contained objects
	for data_collection_object in data_collection_objects:
		data_collection_object.remove()

	# add a dataset
	data_collection.add_object(client.get_project("PROJECT_KEY").get_dataset("DATASET_NAME"))


Reference documentation
=======================

Classes
-------

.. autosummary::
    dataikuapi.dss.data_collection.DSSDataCollection
    dataikuapi.dss.data_collection.DSSDataCollectionItem
    dataikuapi.dss.data_collection.DSSDataCollectionListItem
    dataikuapi.dss.data_collection.DSSDataCollectionPermissionItem
    dataikuapi.dss.data_collection.DSSDataCollectionSettings

Functions
---------
.. autosummary::
    ~dataikuapi.dss.data_collection.DSSDataCollection.add_object
    ~dataikuapi.DSSClient.create_data_collection
    ~dataikuapi.dss.data_collection.DSSDataCollection.delete
    ~dataikuapi.dss.data_collection.DSSDataCollection.get_settings
    ~dataikuapi.DSSClient.list_data_collections
    ~dataikuapi.dss.data_collection.DSSDataCollection.list_objects
    ~dataikuapi.dss.data_collection.DSSDataCollectionItem.remove
