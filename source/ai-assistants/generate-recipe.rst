Generate Recipe 
#####################################

.. contents::
	:local:

.. seealso::
    
	For more information, see also the following article in the Knowledge Base:

    - `Concept | Generate recipes using Generative AI <https://knowledge.dataiku.com/latest/data-preparation/visual-recipes/concept-generate-recipe.html>`_

Setup
======

The Generate Recipe feature is not enabled by default.

Administrators can enable it under Administration > Settings > AI Services > Enable Generate Steps, Recipe, and Metadata.

This also enables:

* The :doc:`AI Prepare / Generate Steps <generate-steps>` feature.
* The :doc:`Generate Metadata <generate-metadata>` feature.

Create a recipe
===============

The feature is accessible from both the flow view and the explore view of a dataset. To use it, select one or multiple datasets from the flow view, then open the right-hand panel where you'll find a new tab labeled "Generate Recipe".
Clicking this tab displays a text input box where you can describe the data preparation steps you want to apply to the selected dataset(s).

.. note::

    To generate visual recipes for multiple datasets, such as join or stack, select all the datasets from the flow that you want to include in the recipe generation context.

Supported recipes
=================

The Generate Recipe feature currently generates only Visual recipes. The supported recipes are:

* Distinct
* Group
* Join
* Pivot
* Prepare
* Sample/Filter
* Sort
* Split
* Stack
* Top n
* Windows
