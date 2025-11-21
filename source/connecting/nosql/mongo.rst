MongoDB
#######

Data Science Studio can both read and write datasets on MongoDB versions 6.0 through 8.1, for which all MongoDB features are supported.

Setting up the MongoDB connection
---------------------------------

Use the `Connection URI` option:

.. code-block:: shell

	mongodb://<USERNAME>:<PASSWORD>@<SHARD HOST>:<PORT (Mongo default = 27017)>/<DATABASENAME>?ssl=true&authSource=admin

As a reminder, be sure to set your connection `Details readable by` a particular group, or all analysts, to ensure access is allowed.
