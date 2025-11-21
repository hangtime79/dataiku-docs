The common editor layout
#########################

All code recipes in DSS use a common layout and UX with a code editor.

Create the recipe
===================

You can create a code recipe

* From the Flow, by clicking on the New recipe button
* From the Flow, in the actions menu of the dataset
* From the Actions menu while being on a dataset

	.. image:: img/dataset-action-menu.png

Select inputs and outputs
---------------------------

A creation modal appears, which lets you:

* Select the input dataset(s)
* Create or select the output dataset(s) or folders

If you have not already selected one, the first step is to select the datasets that are used as "inputs" of your recipe. You may only read in these datasets, not write.

	.. image:: img/new-python-recipe-1.png

You then need to select or create the output datasets. Generally, when you create a recipe, you will be creating its output dataset at the same time. Most times, the output datasets of a recipe will be managed datasets (for more information on Managed datasets, see the :doc:`/concepts/index` page).

	.. image:: img/new-python-recipe-2.png

* Give a name to the output dataset
* Select in which connection it will be stored. For more information about the concept of storing Managed Datasets into connection, see :doc:`/concepts/index`
* You might be able to select storage format and partitioning for your dataset, depending on the storage backends.
* Click on "Create dataset"

You can then create the recipe.

Write code
============

Once you have created your recipe, it is autofilled with "starter" code. This code is here to help you get started, but obviously needs to be modified to suit your needs.

The code should fill data in the output datasets. Please refer to the specific documentation for each recipe for more information about how to do that.

Validate and run the recipe
=============================

Code recipes have a "Run" button that automatically appears as soon as you have defined at least one output dataset for the recipe.

When you click the Run button, a new job is started. When it's over, you get either a success or error message and can explore the generated output datasets.

Most recipes also have a "Validate" button that performs consistency checks in the recipe (for example, check the validity of the code). Some recipes are also able to automatically compute the output schema of your dataset(s). If the current output schema does not match what the recipe wants to output, you'll get prompts to update the output datasets' schemas.