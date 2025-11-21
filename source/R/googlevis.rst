Using googleVis
################

The googleVis package is R interface to Google's chart tools.

For more information, see https://cran.r-project.org/web/packages/googleVis/

Installing googleVis
=====================

The googleVis package is not installed by default. The recommended way to install it is to use a :doc:`code environment </code-envs/index>`

See :doc:`how to install R packages <packages>`

* For a regular R environment, you need to install the ``googleVis`` package
* If you are using a Conda environment, you can also choose instead to install in the Conda section the ``r-googlevis`` package.

Displaying charts in a Jupyter notebook
=========================================

googleVis charts will not work properly if you only use the ``plot()`` method in a Jupyter R notebook.

Instead, use the ``dkuDisplayGooglevis`` method.

For example; to display the first example in the googleVis documentation:

.. code-block:: R

	library(googleVis)

	# Make some data
	df=data.frame(country=c("US", "GB", "BR"), 
              val1=c(10,13,14), 
              val2=c(23,12,32))

    # Prepare the chart
    Line <- gvisLineChart(df)

    # And display it
    dkuDisplayGooglevis(Line)

Displaying charts on a dashboard
=========================================

googleVis charts generated using R code can be shared on a DSS dashboard using the "static insights" system.

Each chart can become a single insight in the dashboard. 

To do so, create :doc:`static insights </R-api/static_insights>`

.. code-block:: R

	# Prepare thje chart
	Line <- gvisLineChart(df)

	# Save it as an insight
	dkuSaveGooglevisInsight("my-googlevis-plot", Line)

From the Dashboard, you can then add a new "Static" insight, select the ``my-googlevis-plot`` insight

Refreshing charts on a dashboard
---------------------------------

You can refresh the charts automatically on a dashboard by using a scenario to re-run the above piece of code.

This call to ``dkuSaveGooglevisInsight`` code can be:

* In a DSS recipe (use a regular "Build" scenario step)
* In a Jupyter notebook (use a "Export notebook" scenario step)
