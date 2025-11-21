Creating an API endpoint for using an LLM-Based agent
*****************************************************

.. admonition:: Deprecated
    :class: attention

    This tutorial is deprecated as of the introduction of the Agent API: :doc:`/tutorials/plugins/agent/generality/index`.

In this tutorial, you will learn how to create an API endpoint using a headless API webapp for an LLM-based agent.
This tutorial is based on two tutorials: :doc:`/tutorials/genai/agents-and-tools/agent/index` and
:doc:`/tutorials/webapps/common/api/index`.
You will use Dash as the applicative framework, but you can quickly adapt this tutorial to your preferred framework.
You can directly jump to :ref:`this section<tutorial-webapps-dash-api-agent-defining-routes>` if you already have a working LLM-based agent.

Prerequisites
#############

* Dataiku >= 13.1
* You must download :download:`this dataset<./assets/pro_customers.csv>` and
  create an **SQL** dataset named ``pro_customers_sql``.
* A code environment with the following packages:

  .. code-block:: python

    dash
    langchain==0.2.0
    duckduckgo_search==6.1.0


Tools' definition
#################

You will define the external tools your LLM agent will use, as you defined in the previous tutorial.
In our case, these tools include:

* **Dataset lookup tool**: used to execute SQL queries on the ``pro_customers_sql`` dataset
  to retrieve customer information (name, role, company), given a customer ID.
  :ref:`Code 1<tutorial-webapps-dash-api-agent-dataset-lookup-code>` shows an implementation of this tool.
* **Internet search tool**: used to perform internet searches to fetch more detailed information
  about the customer’s company.
  :ref:`Code 2<tutorial-webapps-dash-api-agent-internet-search-code>` shows an implementation of this tool.

.. literalinclude:: ./assets/app.py
    :language: python
    :caption: Code 1: Dataset lookup tool
    :name: tutorial-webapps-dash-api-agent-dataset-lookup-code
    :lines: 6-10,20-46

.. literalinclude:: ./assets/app.py
    :language: python
    :caption: Code 2: Internet search tool
    :name: tutorial-webapps-dash-api-agent-internet-search-code
    :lines: 11-12,48-74

LLM agent creation
##################

With the tools defined, the next step is to create an agent that can effectively utilize these tools.
This tutorial uses the `ReAct <https://react-lm.github.io/>`__ logic,
which combines the LLM’s ability for reasoning (e.g., chain-of-thought prompting, etc.)
and acting (e.g., interfacing with external software, etc.) through a purposely crafted prompt.

.. literalinclude:: ./assets/app.py
    :language: python
    :caption: Code 3: LLM agent creation
    :name: tutorial-webapps-dash-api-agent-llm-creation-code
    :lines: 3-4,13-19,77-105


.. _tutorial-webapps-dash-api-agent-defining-routes:

Defining the routes
###################

The first step is to define the routes you want your API to handle.
A single route is responsible for a (simple) process.
Dataiku provides an easy way to describe those routes.
Relying on a Flask server helps you return the desired resource types.
Check the API access in the web apps’ settings to use this functionality, as shown in Figure 1.


.. _tutorial-webapps-dash-api-agent-access:

.. figure:: ./assets/tutorial-webapps-dash-api-agent-access.png
    :align: center
    :class: with-shadow image-popup
    :alt: Figure 1: Enabling API access.

    Figure 1: Enabling API access.

This tutorial relies on a single route parametrized by the customer's ID to query the LLM
and give the user the appropriate answer.
Once you have set the code env in the settings panel, you will define the route, as shown in Code 4.

.. literalinclude:: ./assets/app.py
    :language: python
    :caption: Code 4: Route handling
    :name: tutorial-webapps-dash-api-agent-routes-code
    :lines: 108-125

Testing the API
###############

Once you have set up everything, you may test your API.
Testing the API can be done in different ways.
They are all required to know the ``WEBAPP_ID`` and the ``PROJECT_KEY``.
The ``WEBAPP_ID`` is the first eight characters (before the underscore) in the webapp URL.
For example, if the webapp URL in Dataiku is ``/projects/HEADLESS/webapps/kUDF1mQ_api/view``,
the ``WEBAPP_ID`` is ``kUDF1mQ``, and the ``PROJECT_KEY`` is ``HEADLESS``.
Additionally, you may need an API key to test the API, depending on the way you want to access your API.
Please read :doc:`this documentation<refdoc:apinode/security>` if you need help setting up an API key.

Via browser
^^^^^^^^^^^

In a browser, enter the URL:

.. code-block::

    http://<DATAIKU_ADDRESS>:<DATAIKU_PORT>/web-apps-backends/<PROJECT_KEY>/<WEBAPP_ID>/get_customer_info/<customer_ID>

This will require the user to be logged to access to this resource.


Via command line
^^^^^^^^^^^^^^^^

Using ``cUrl`` requires an API key to access the headless API or an equivalent way of authenticating,
depending on the authentication method set on the Dataiku instance.

.. code-block::

    curl -X GET --header 'Authorization: Bearer <USE_YOUR_API_KEY>' \
        'http://<DATAIKU_ADDRESS>:<DATAIKU_PORT>/web-apps-backends/<PROJECT_KEY>/<WEBAPP_ID>/get_customer_info/<customer_ID>'


Via Python
^^^^^^^^^^

You can access the headless API using the Python API.
Depending on whether you are inside Dataiku or outside, you will use the ``dataikuapi`` or the ``dataiku`` package,
respectively, as shown in :ref:`Code 5<tutorial-webapps-dash-api-agent-testing-python-code>`.

.. literalinclude:: ./assets/python.py
    :language: python
    :caption: Code 5: Testing the API from Python
    :name: tutorial-webapps-dash-api-agent-testing-python-code

Wrapping up
###########

Congratulations!
You have completed this tutorial and have a working API serving an agent.
You can try to tweak the agent or integrate this API into a more complex process.

Here is the complete code of the headless web application:

.. dropdown:: :download:`app.py<./assets/app.py>`
    :open:

    .. literalinclude:: ./assets/app.py
        :language: python
