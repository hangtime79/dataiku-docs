Visual recipes
###############

In the Flow, recipes are used to create new datasets by performing transformations on existing datasets. The main way to perform transformations is to use the DSS "visual recipes", which cover a variety of common analytic use cases, like aggregations or joins.

By using visual recipes, you don't need to write any code to perform the standard analytic transformations.

Visual recipes are not the only way to perform transformations in the Flow. You can also use :doc:`code recipes </code_recipes/index>`, for example with SQL or HiveQL queries, or with Python or R. These code recipes offer you complete freedom for analytic cases which are not covered by DSS visual recipes.

.. toctree::

	prepare
	sync
	grouping
	window
	distinct
	join
	fuzzy-join
	geojoin
	split
	topn
	stack
	sampling
	sort
	pivot
	generate-features
	generate-statistics
	push-to-editable
	download
	list-folder-contents
	dynamic-repeat
	generate-recipe
	extract-failed-rows
	upsert
	list-access
