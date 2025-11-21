Using Bokeh
##############

Bokeh is a Python interactive visualization library that provides interactive plots and dashboards. There are several ways you can use Bokeh in DSS:

* For fully-interactive interaction (multiple charts, various controls, ...), by creating a :doc:`Bokeh webapp </webapps/index>`
* To display interactive (pan/zoom/...) charts within a Jupyter notebook
* To display interactive (pan/zoom/...) charts on a Dashboard

Documentation for Bokeh is available at https://bokeh.pydata.org

Installing Bokeh
==================

You need to install the `Bokeh` package in a :doc:`code environment </code-envs/index>`.

Creating a Bokeh interactive web application
=============================================

See :doc:`/webapps/index`

Displaying charts in a Jupyter notebook
=========================================

To display plot.ly charts in a Jupyter notebook, use this cell once in the notebook:

.. code-block:: python

	from bokeh.io import output_notebook, show
	output_notebook()

You can then use ``show()`` to show Bokeh figures

For example, to display a chart showing simple circles:

.. code-block:: python

	from bokeh.plotting import figure

	f = figure()
	f.circle([1,2,3], [4,5,6], size=10)

	show(f)

A complete documentation for the usage of Bokeh in a Jupyter notebook can be found at https://docs.bokeh.org/en/latest/docs/user_guide/output/jupyter.html

Using interactive controls in the Jupyter notebook
---------------------------------------------------

You can use interactive controls (sliders, inputs, ...) that are displayed in the notebook. When you change these controls, the Bokeh chart can react dynamically.

Documentation for this is available here: https://docs.bokeh.org/en/latest/docs/user_guide/output/jupyter.html#jupyter-interactors

Displaying Bokeh charts on a dashboard
=========================================

Bokeh charts generated using Python code can be shared on a DSS dashboard using the "static insights" system. This does not include the capability to include controls. If you want to use Bokeh controls on a DSS Dashboard, use a Bokeh webapp.

Each Bokeh figure can become a single insight in the dashboard. Each chart will retain full zoom/pan/select/export capabilities;

To do so, create :doc:`static insights <devguide:api-reference/python/static-insights>`

.. code-block:: python

	from dataiku import insights

	# f is a Bokeh figure, or any object that can be passed to show()

	insights.save_bokeh("my-bokeh-plot", f)

From the Dashboard, you can then add a new "Static" insight, select the ``my-bokeh-plot`` insight

Refreshing charts on a dashboard
---------------------------------

You can refresh the charts automatically on a dashboard by using a scenario to re-run the above piece of code.

This call to ``dataiku.insights`` code can be:

* In a DSS recipe (use a regular "Build" scenario step)
* In a Jupyter notebook (use a "Export notebook" scenario step)
* As a custom Python scenario step

Displaying images in Bokeh 
=========================================

To plot images in Bokeh, the image path specified must be relative to your “current location”.  

You can plot images in a Jupyter notebook or display them in a webapp. 

Images can be stored in ``DATADIR/local/static``. An administrator can upload images to the DSS UI by going to Global Shared Code > Static Web Resources > +Add.   

In a Jupyter notebook
---------------------------------------------------

Here’s an example of displaying an image in a Jupyter notebook:

.. code-block:: python

	import dataiku
	from bokeh.plotting import figure, show
	from bokeh.io import output_notebook

	path = '/local/static/cat-image.jpg'
	f = figure(x_range=(0,1), y_range=(0,1), width=1000, height=500)
	f.image_url(url=[path], x=0, y=0, w=1, h=1, anchor='bottom_left')
 	output_notebook()
	show(f)

In a webapp 
---------------------------------------------------

From a webapp, you’ll need to refer to the relative path to your image.

To refer to the image saved in ``DATADIR/local/static`` from a Bokeh webapp, you can use the relative path from the webapp directory: 

.. code-block:: python

    import os
    from bokeh.plotting import figure
    from bokeh.layouts import row, widgetbox
    from bokeh.io import curdoc

    # get the full path to the image, and convert it to a relative path for the webapp 
    full_path = os.path.join(os.environ["DIP_HOME"], 'local/static/cat-image.jpg')
    relative_path = os.path.relpath(full_path)
    
    plot = figure(x_range=(0,1), y_range=(0,1), width=1000, height=500)
    plot.image_url(url=[relative_path], x=0, y=0, w=1, h=1, anchor='bottom_left')
    curdoc().add_root(row(plot, width=800))

For webapps, the image should be small enough to ensure a reasonable load time. 
