DSS and R
###############

DSS includes deep integration with R. In many parts of DSS, you can write R code:

* In recipes (both regular R, SparkR and Sparklyr)
* In Jupyter notebooks
* For Shiny webapps
* In plugins
* In API node, for  :doc:`custom prediction models </apinode/endpoint-r-prediction>` or :doc:`custom functions </apinode/endpoint-r-function>`  endpoints

Any R package may be used in DSS.

In addition, DSS features a complete R API, which has its own :doc:`documentation </R-api/index>`.

The following highlights how a few specific R packages can be used in DSS. DSS features advanced integration with most of the packages described below.

DSS also has :doc:`integration with RStudio <rstudio>`

On Dataiku Cloud, R can be installed by activating the R integration extension in the Extension tab of the Launchpad.

.. toctree::

	packages
	reusing-code
	rmarkdown
	ggplot2
	dygraphs
	googlevis
	ggvis
	prophet
	rstudio

