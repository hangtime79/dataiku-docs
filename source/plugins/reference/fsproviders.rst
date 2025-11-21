Component: Filesystem providers
################################

FS providers give DSS a way to interact with external systems by exposing them as filesystem-like. The user can them access the data stored on these systems using the same concepts as other filesystem-based datasets (HDFS, S3,...). "Filesystem-like" means first and foremost that data is stored in objects that are hierarchized, and that the content of these objects can be read and written with a streaming API. More specifically, the capabilities of a FS provider are:

* define objects by means of a path
* list objects located at a given path, or contained by a given path
* read/write the data as a stream of bytes
* delete objects contained by a given path
* move objects from a path to another


Paths
=====

DSS will identify objects accessed through the FS provider by paths. A path is a '/'-separated list of object names, and it needs to be unique for each object. Just like for regular filesystems, there is a root denoted by '/' and the path is understood as left-to-right containment, i.e. '/a/b/c' denotes object 'c' inside object 'b' inside object 'a' inside the root '/'.

Containment of other objects defines a dichotomy between directories and files:

* a directory holds no data by itself, only other objects (directories or filed)
* a file doesn't contain any object, only data

Note that directories need not actually exist on the external system, as long as the containment rule is enforced (this is the case for blob storages like S3, Azure Blob Storage, or Google Cloud Storage). In this case, the FS provider doesn't need to bother with the concept of empty directories.


Creating a custom FS provider
=============================

To start creating a FS provider,  we recommend that you use the plugin developer tools (see the tutorial for an introduction). In the Definition tab, click on "Add Component", pick the FS provider type and enter the identifier for your new FS provider. You'll see a new folder ``python-fs-providers`` and will have to edit the ``fs-provider.py`` and ``fs-provider.json`` files. The starter code is a simple provider which reads/writes from the local filesystem, starting at a path set in the provider's parameters.

A FS provider is a :py:class:`Python class <dataiku.fsprovider.FSProvider>`, with methods for each function it needs to handle:


Instantiation and teardown
--------------------------

The :py:class:`constructor <dataiku.fsprovider.FSProvider>`  is called with the parameters set by the user in the dataset's form and with a path denoting the dataset's root. Contrary to other datasets, there is no "connection" concept, so each dataset using the custom FS provider has to (re)define values for the parameters. The instance of the FS provider is expected to handle all path parameters passed to its methods as relative to the dataset root.

The :py:meth:`close() method <dataiku.fsprovider.FSProvider.close>` is called when the instance of the FS provider is not needed anymore, before killing the Python process running its code, to give some time to perform cleanup actions if necessary


Object inspection and listing
-----------------------------

The :py:meth:`stat() method <dataiku.fsprovider.FSProvider.stat>` is expected to return a description of the object located at the given path. The :py:meth:`browse() method <dataiku.fsprovider.FSProvider.browse>` is expected to return the same information as stat(), together with a listing of the objects directly under the object at the given path when it's a directory. The :py:meth:`enumerate() method <dataiku.fsprovider.FSProvider.enumerate>` is expected to return the list of all files, not directories, contained in a given path (recursively).


Object modifications
--------------------

The :py:meth:`delete_recursive() method <dataiku.fsprovider.FSProvider.delete_recursive>` is expected to remove all object at or contained by the given path. The :py:meth:`set_last_modified() method <dataiku.fsprovider.FSProvider.set_last_modified>` should, when possible, change the modification time of the object defined by the given path. If modification times don't exist, or can't be changed, the method should simply not do anything. The :py:meth:`move() method <dataiku.fsprovider.FSProvider.move>` is expected to change the identifying path of a given object.


Data read/write
---------------

Data access is done by means of byte streams. The streams are not seekable.
