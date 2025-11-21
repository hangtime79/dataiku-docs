Using ggvis
############

ggvis is a data visualization package for R

For more information, see http://ggvis.rstudio.com/

Installing ggvis
=====================

Installing the ggvis package
-----------------------------

The ggvis package is not installed by default. The recommended way to install it is to use a :doc:`code environment </code-envs/index>`

See :doc:`how to install R packages <packages>`

* For a regular R environment, you need to install the ``ggvis`` package
* If you are using a Conda environment, you can also choose instead to install in the Conda section the ``r-ggvis`` package.

Installing the frontend dependencies
-------------------------------------

To work, ggvis first needs some frontend libraries, that need to be preinstalled once.

To install the dependencies, open a R notebook and run

.. code-block:: R

	library(dataiku)
	dkuInstallGgvisDependenciesOnce()

.. warning::

	It is not possible to run this if your DSS instance has the User Isolation Framework enabled.

	In that case, your DSS administrator needs to run this from a command-line ./bin/R prompt, after
	setting the DIP_HOME env variable to the location of the DSS data directory


Displaying charts in a Jupyter notebook
=========================================

ggvis charts will not work properly if you only enter it in a Jupyter notebook

Instead, use the ``dkuDisplayGgvis`` method.

For example; to display the first example in the ggvis documentation:

.. code-block:: R

	library(dataiku)
	library(ggvis)

	# Prepare the chart
	chart <- mtcars %>% ggvis(~wt, ~mpg) %>% layer_points()

    # And display it
    dkuDisplayGgvis(Line)

Displaying charts on a dashboard
=========================================

googleVis charts generated using R code can be shared on a DSS dashboard using the "static insights" system.

Each chart can become a single insight in the dashboard.

To do so, create :doc:`static insights </R-api/static_insights>`

.. code-block:: R

	# Prepare the chart
	chart <- mtcars %>% ggvis(~wt, ~mpg) %>% layer_points()

	# Save it as an insight
	dkuSaveGgvisInsight("my-ggvis-plot", chart)

From the Dashboard, you can then add a new "Static" insight, select the ``my-ggvis-plot`` insight

Plots can be donwloaded in SVG or PNG format

Refreshing charts on a dashboard
---------------------------------

You can refresh the charts automatically on a dashboard by using a scenario to re-run the above piece of code.

This call to ``dkuSaveGgvisInsight`` code can be:

* In a DSS recipe (use a regular "Build" scenario step)
* In a Jupyter notebook (use a "Export notebook" scenario step)
