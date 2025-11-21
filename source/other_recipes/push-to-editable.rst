Push to editable recipe
########################

.. contents::
	:local:

The "Push to editable" recipe allows you to copy a regular dataset to an Editable Dataset while keeping changes. Since Editable Datasets are limited to 100K rows, so are push to editable recipes. See :doc:`/connecting/editable-datasets` for more information about Editable Datasets.

The first time you run a Push to editable recipe, it will copy the whole content of the regular dataset to the editable dataset. If you make changes to the content in the editable dataset, and then rerun the push to editable recipe, it will copy over all data that was new or changed in the original dataset but will preserve every modification you did in the editable dataset.

To identify what is considered as "new" or "was modified in editable dataset", you need to select one or several columns that will form a unique identifier.

The main use case for a push to editable recipe is to make  manual corrections to a dataset. 
For example, you have an input dataset of product categories in a database, but there are some errors, and for some reason, you can't get the error to be fixed in the source data: you use a push to editable recipe, fix the erroneous entries, and base the rest of the flow on the editable dataset.


Creating a Push to Editable recipe
===================================

From the Flow, click the "+Recipe" button, and select Visual > Push to editable.
Alternatively if you have selected a dataset, go to the right panel's Action tab, and select Other recipes > Push to editable.

Give a name to the output editable dataset. 

Create the recipe. Select one or several columns to use as the unique identifier for each row.

You can also use the Filter section to remove data from your dataset. The filters documentation is available :doc:`here  <../other_recipes/sampling>`.
