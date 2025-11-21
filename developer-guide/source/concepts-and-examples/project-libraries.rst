Project libraries
##################

..
  this code samples has been verified on DSS: 13.2.0
  Date of check: 25/09/2024

  this code samples has been verified on DSS: 14.2.0
  Date of check: 17/09/2024

You can interact with the Library of each project through the API.

Getting the DSSLibrary object
==============================

You must first retrieve the :py:class:`~dataikuapi.dss.projectlibrary.DSSLibrary` through the :py:meth:`~dataikuapi.dss.project.DSSProject.get_library` method

.. code-block:: python

    project = client.get_project("MYPROJECT")
    library = project.get_library()

Retrieving the content of a file
=================================

.. code-block:: python

    library_file = library.get_file("/file.txt")
    print("Content: %s" % library_file.read())

    # Alternate ways to retrieve a file handle
    library_file = library.get_file("/python/some_code.py")
    library_file = library.get_folder("/").get_file("file.txt")

Getting the list of all the library items
==========================================

.. code-block:: python

    def print_library_items(item):
        print(item.path)
        if "list" in dir(item):
            for child in item.list():
                print_library_items(child)

    for item in library.list():
        print_library_items(item)

Add a new folder in the library
================================

.. code-block:: python

    library.add_folder("/new_folder")
    library.add_folder("/python/new_sub_folder")
    library.get_folder("/python").add_folder("another_sub_folder")

Add a new file in the library
==============================

.. code-block:: python

    with open("/path/to/local/file", "rb") as file:
        new_txt_file = library.add_file("/new_folder/new_file.txt")
        new_txt_file.write(file)

    with open("/path/to/local/file", "rb") as file:
        new_json_file = library.get_folder("/new_folder").add_file("new_file.json")
        new_json_file.write(file)


Rename a file or a folder in the library
=========================================

.. code-block:: python

    # rename a file in the library
    library.get_file("/folder/file.txt").rename("renamed_file.txt")

    # rename a folder in the library
    library.get_folder("/folder").rename("renamed_folder")

Move a file or a folder in the library
=======================================

.. code-block:: python

    # move a file in the library
    library.get_file("/folder/file.txt").move_to(library.get_folder("/folder2"))

    # move a folder in the library
    library.get_folder("/folder").move_to(library.get_folder("/folder2"))

Delete a file or a folder from the library
==========================================

.. code-block:: python

    library.get_file("/path/to/item").delete()
    library.get_folder("/path/to").get_file("/item").delete()
    library.get_folder("/path/to").delete()

Reference documentation
========================

Classes
-------

.. autosummary::
    dataikuapi.dss.projectlibrary.DSSLibraryFolder
    dataikuapi.dss.projectlibrary.DSSLibrary
    dataikuapi.dss.projectlibrary.DSSLibraryFile

Functions
---------

.. autosummary::
    ~dataikuapi.dss.projectlibrary.DSSLibrary.add_folder
    ~dataikuapi.dss.projectlibrary.DSSLibraryFile.delete
    ~dataikuapi.dss.projectlibrary.DSSLibraryFolder.delete
    ~dataikuapi.dss.projectlibrary.DSSLibraryFolder.add_folder
    ~dataikuapi.dss.projectlibrary.DSSLibrary.get_file
    ~dataikuapi.dss.projectlibrary.DSSLibrary.get_folder
    ~dataikuapi.dss.project.DSSProject.get_library
    ~dataikuapi.dss.projectlibrary.DSSLibrary.list
    ~dataikuapi.dss.projectlibrary.DSSLibraryFolder.list
    ~dataikuapi.dss.projectlibrary.DSSLibraryFile.move_to
    ~dataikuapi.dss.projectlibrary.DSSLibraryFolder.move_to
    ~dataikuapi.dss.projectlibrary.DSSLibraryFile.read
