Component: Web Apps
###################

Web apps can be turned into plugins. This allows you to have reusable and instantiable web apps, such as custom visualizations for datasets.

To create a web app component, you need to first create a normal web app, and then use Advanced > Convert to plugin web app.

.. seealso::

    A tutorial on this plugin component is available in the Developer Guide: :doc:`devguide:tutorials/plugins/webapps/index`.


The primary files for a web app component are a *webapp.json* file that defines the parameters for the web app, and one or more files adapted from the normal web app that define the web app itself.

For an HTML/Javascript web app, there will be *app.js*, *body.html* and *style.css* files that define the Javascript, HTML, and CSS for the web app.  Use the  ``dataiku.getWebAppConfig()`` method to extract parameter values the user specifies on the web app Settings tab.  For example, the following code snippet pulls the user-specified value of the ``dataset`` parameter and assigns it to a variable ``dataset``.

.. code-block:: javascript

  let dataset = dataiku.getWebAppConfig()['dataset'];


For a Python Bokeh or Dash web app, there will be a *backend.py* file.  Use the  ``get_webapp_config()`` method to extract parameter values the user specifies on the web app Settings tab.  For example, the following code snippet pulls the user-specified value of the ``input_dataset`` parameter and assigns it to a variable ``input_dataset``.

.. code-block:: python

  input_dataset = get_webapp_config()['input_dataset']


For an R Shiny web app, there will be *server.R* and *ui.R* files.  Use the  ``dataiku::dkuPluginConfig()`` method to extract parameter values the user specifies on the web app Settings tab.  For example, the following code snippet pulls the user-specified value of the ``input_dataset`` parameter and assigns it to a variable ``input_dataset``.

.. code-block:: r

  input_dataset = dkuPluginConfig()['input_dataset']
