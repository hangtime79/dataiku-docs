Using ggplot2
##############

The ggplot2 package offers a powerful graphics language for creating elegant and complex plots. 

For more information, see http://ggplot2.org/

Installing ggplot2
===================

The ggplot2 package is installed in the builtin R environment of DSS. If you are using a custom code environment, you'll need to install it.

See :doc:`how to install R packages <packages>`

* For a regular R environment, you need to install the ``ggplot2`` package
* If you are using a Conda environment, you can also choose instead to install in the Conda section the ``r-ggplot2`` package.

Displaying charts in a Jupyter notebook
=========================================

ggplot2 charts display naturally inthe Jupyter notebook.

For example, if "df" is a dataframe obtained with ``dkuReadDataset`` with columns "age" and "price", you can make a scatter plot with 
a smoothing line with

.. code-block:: R

	library(ggplot2)

	ggplot(df, aes(x = age)) 
		+ geom_point( aes(y = price))
		+ geom_smooth( aes(y = price))


Displaying charts on a dashboard
=========================================

ggplot2 charts generated using R code can be shared on a DSS dashboard using the "static insights" system.

Each chart can become a single insight in the dashboard. 

To do so, create :doc:`static insights </R-api/static_insights>`

You can either save the last displayed plot:

.. code-block:: R

	# Display a plot
	ggplot(df, aes(x=myXColumn, y=myYColumn)) + geom_point()

	# Save it as an insight
	dkuSaveGgplotInsight("my-ggplot2-plot")

Or save an explicit plot object:

.. code-block:: R

	# Prepare a plot object
	gg <- ggplot(df, aes(x=myXColumn, y=myYColumn)) + geom_point()

	# Save it as an insight
	dkuSaveGgplotInsight("my-ggplot2-plot", gg)

From the Dashboard, you can then add a new "Static" insight, select the ``my-ggplot2-plot`` insight

Refreshing charts on a dashboard
---------------------------------

You can refresh the charts automatically on a dashboard by using a scenario to re-run the above piece of code.

This call to ``dkuSaveGgplotInsight`` code can be:

* In a DSS recipe (use a regular "Build" scenario step)
* In a Jupyter notebook (use a "Export notebook" scenario step)

Using in Shiny
===============

ggplot2 can be used directly in Shiny, inside of a ``renderPlot`` block.