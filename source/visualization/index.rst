Charts
############################

Charts are visual aggregations of data that provide insight into the relationships in your datasets.

DSS delivers an advanced data visualization engine through the Charts tab of a dataset or visual analysis.  The chart-building interface is essentially the same in both locations, with the following important caveats.

- Charts in a visual analysis can work in real-time on the output of a data preparation Script. Instead of rebuilding a dataset, simply add a step to the script and view the result immediately.
- Charts in a dataset can be published as insights for inclusion in dashboards, while charts in a visual analysis cannot.  However, when a visual analysis is deployed as a Prepare recipe, its charts can be transferred during deployment to the output dataset.
- Charts in a dataset can make use of the in-database :doc:`execution engine <sampling>`, while charts in a visual analysis are always run in the DSS engine.

.. seealso::
    For more information, see the `Charts <https://knowledge.dataiku.com/latest/data-viz/charts/index.html>`_ section in the Knowledge Base.

****

.. toctree::
	interface
	sampling
	charts-basics
	charts-tables
	charts-scatters
	charts-maps
	charts-other
	common
	palettes
	formatting
	filter-settings
	custom-aggregations
	reusable-dimensions
	reference-lines
	copy-paste
	third-party-bi-tools
