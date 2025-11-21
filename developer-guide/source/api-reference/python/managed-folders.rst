:tocdepth: 2

Managed folders
################

.. note::

    There are two main classes related to managed folder handling in Dataiku's Python APIs:

    * :class:`dataiku.Folder` in the `dataiku` package. It was initially designed for usage within DSS in recipes and Jupyter notebooks.

    * :class:`dataikuapi.dss.managedfolder.DSSManagedFolder` in the `dataikuapi` package. It was initially designed for usage outside of DSS.

    Both classes have fairly similar capabilities, but we recommend using `dataiku.Folder` within DSS.

For usage information and examples, see :doc:`/concepts-and-examples/managed-folders`

dataiku package
================

.. autoclass:: dataiku.Folder
    :members:

dataikuapi package
====================

Use this class preferably outside of DSS

.. automodule:: dataikuapi.dss.managedfolder
    :members:
    :member-order: bysource
    :undoc-members: