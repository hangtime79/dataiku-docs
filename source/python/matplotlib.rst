Using Matplotlib
##################


Matplotlib is a Python plotting library which produces a large variety of visuals. There are several ways you can use Matplotlib in DSS:

* To display charts within a Jupyter notebook
* To display charts on a Dashboard

Documentation for Matplotlib is available at https://matplotlib.org/

Installing Matplotlib
=======================

* If you are using the DSS built-in environment, Matplotlib is already installed. You don't need to do any specific installation
* If you are using a  :doc:`code environment </code-envs/index>`, you need to install the `matplotlib` package


Displaying charts in a Jupyter notebook
=========================================

To display Matplotlib charts in a Jupyter notebook, the easiest is to simply execute the first cell of the notebook:

.. code-block:: python

	%pylab inline

This automatically imports the ``matplotlib`` and ``matplotlib.pyplot as plt`` packages. It also imports ``numpy as np``.

You can then use the regular Matplotlib functions.

For example, to reproduce the simplest sample "sin" figure, use:

.. code-block:: python

	# Data for plotting
	t = np.arange(0.0, 2.0, 0.01)
	s = np.sin(2 * np.pi * t)

	plt.plot(t, s)

The chart displays inline in the Jupyter notebook

Displaying Matplotlib charts on a dashboard
=============================================

Matplotlib charts generated using Python code can be shared on a DSS dashboard using the "static insights" system. -

Each Matplotlib figure can become a single insight in the dashboard.

To do so, create :doc:`static insights <devguide:api-reference/python/static-insights>`

.. code-block:: python

	from dataiku import insights

	# This form saves the last displayed figure
	insights.save_figure("my-matplotlib-plot")

	# If f is a matplotlib figure object, you can save explicitly this figure
	# rather than the last displayed one

	insights.save_figure("my-matplotlib-explicit-plot", f)

From the Dashboard, you can then add a new "Static" insight, select the ``my-matplotlib-plot`` insight

Refreshing charts on a dashboard
---------------------------------

You can refresh the charts automatically on a dashboard by using a scenario to re-run the above piece of code.

This call to ``dataiku.insights`` code can be:

* In a DSS recipe (use a regular "Build" scenario step)
* In a Jupyter notebook (use a "Export notebook" scenario step)
* As a custom Python scenario step


Using matplotlib in a recipe
=============================

Matplotlib is based on a concept of backends. Each backend knows how to display figures. When running Python on your local machine, Matplotlib will by default pop a graphical window (a Windows, macOS or Linux window) to show each plot. This is done using a specific backend for each OS.

In a notebook, when using ```%pylab inline```, it automatically activates a specific backend that displays the plots inline within the Jupyter interface.

In a recipe or in a custom Python scenario step, the notebook backend is not available. You must thus, as the very first action in your recipe, use the following code:


.. code-block:: python

	import matplotlib
	matplotlib.use("Agg")

This forces the use of the "Agg" backend which performs rendering of the charts in-memory. Charts can then be exported to PNG, ...

.. warning::

	This ``matplotlib.use("Agg")`` must take place before ``import matplotlib.pyplot``. Failure to do so will generally result in an error with "Tkinter". This error is caused by the fact that Matplotlib will by default try to import a backend called "TCL/TK" which is based on the "Tkinter" Python library, which is not usually installed
