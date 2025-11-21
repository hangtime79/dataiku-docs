Creating a Gradio application using an LLM-based agent
******************************************************


In this tutorial, you will learn how to build an Agent application using Gradio.
You will build an application to retrieve customer and company information based on a login.
This tutorial relies on two tools.
One tool retrieves a user's name, position, and company based on a login.
This information is stored in a Dataset.
A second tool searches the Internet to find company information.

This tutorial is based on the :doc:`/tutorials/genai/agents-and-tools/agent/index` tutorial.
It uses the same tools and agents in a similar context.
If you have followed this tutorial, you can jump to the :ref:`webapp-gradio-agent-creating-the-gradio-application` section.

Prerequisites
#############

* Administrator permission to build the template
* An LLM connection configured
* A Dataiku version > 12.6.2
* A code environment (named ``gradio-and-agents``) with the following packages:

  .. code-block:: python

    gradio <4
    langchain==0.2.0
    duckduckgo_search==6.1.0


Building the Code Studio template
#################################

If you know how to build a Code Studio template using Gradio and a dedicated code environment,
you have to create one named ``gradio-and-agent``.

If you don't know how to do it, please follow these instructions:

* Go to the **Code Studios** tab in the **Administration** menu, click the **+Create Code Studio template** button,
  and choose a meaningful label (``gradio_template``, for example).
* Click on the **Definition** tab.
* Add a new **Visual Studio Code** block.
  This block will allow you to edit your Gradio application in a dedicated Code Studio.
* Add the **Add Code environment** block, and choose the code environment previously created (``gradio-and-agents``).
* Add the **Gradio** block and select the code environment previously imported, as shown in Figure 1.
* Click the **Save** button.
* Click the **Build** button to build the template.

.. _webapp-gradio-agent-code-studio-gradio-block:

.. figure:: ./assets/webapp-gradio-agent-code-studio-gradio-block.png
    :align: center
    :class: with-shadow image-popup
    :alt: Figure 1: Code Studio -- Gradio block.
    
    Figure 1: Code Studio -- Gradio block.
    

Your Code Studio template is ready to be used in a project.

Creating the Agent application
##############################

Preparing the data
^^^^^^^^^^^^^^^^^^
You need to create the associated dataset,
as you will use a dataset that stores a user's ID, name, position, and company based on that ID.

.. _webapp-gradio-agent-table1:
.. csv-table:: Table 1: customer ID
   :file: ./assets/pro_customers.csv
   :header-rows: 1


:ref:`Table 1<webapp-gradio-agent-table1>`, which can be downloaded :download:`here<./assets/pro_customers.csv>`,
represents such Data.
Create a SQL Database named ``pro_customers_sql`` by uploading the CSV file
and using a **Sync recipe** to store the data in an SQL connection.


Creating utility functions
^^^^^^^^^^^^^^^^^^^^^^^^^^

Be sure to have a valid ``LLM ID`` before creating your Gradio application.
The :ref:`documentation<ce/llm-mesh/get-llm-id>` provides instructions on obtaining an ``LLM ID``.

* Create a new project, click on **</> > Code Studios**.
* Click the **+New Code Studio**, choose the previously created template, choose a meaningful name,
  click the **Create** button, and then click the **Start Code Studio** button.
* To edit the code of your Gradio application, click the highlighted tabs (VS Code) as shown in
  :ref:`Figure 2<webapp-gradio-agent-code-studio>`.

  .. _webapp-gradio-agent-code-studio:
  
  .. figure:: ./assets/webapp-gradio-agent-code-studio.png
      :align: center
      :class: with-shadow image-popup
      :alt: Figure 2: Code studio -- Edit the code.
      
      Figure 2: Code studio -- Edit the code.
      
* Select the ``gradio`` subdirectory in the ``code_studio-versioned`` directory.
  Dataiku provides a sample application in the file ``app.py``.

You will modify this code to build the application.
The first thing to do is define the different tools the application needs.
There are various ways of defining a tool.
The most precise one is based on defining classes that encapsulate the tool.
Alternatively, you can use the ``@tool`` annotation or the ``StructuredTool.from_function`` function,
but it may require more work when using those tools in a chain.

To define a tool using classes, there are two steps to follow:

* Define the interface: which parameter is used by your tool.
* Define the code: how the code is executed.


:ref:`Code 1<webapp-gradio-code-get-customer-info>` shows how to describe a tool using classes.
The highlighted lines define the tool's interface.
This simple tool takes a customer ID as an input parameter and runs a query on the SQL Dataset.

.. literalinclude:: ./assets/app.py
    :language: python
    :caption: Code 1: Get customer's information
    :name: webapp-gradio-code-get-customer-info
    :lines: 26-52
    :emphasize-lines: 1-3

.. attention::
    The SQL query might be written differently depending on your SQL Engine.


Similarly, :ref:`Code 2<webapp-gradio-code-get-company-info>` shows how to create a tool that searches the Internet for information on a company.

.. literalinclude:: ./assets/app.py
    :language: python
    :caption: Code 2: Get company's information
    :name: webapp-gradio-code-get-company-info
    :lines: 54-77
    :emphasize-lines: 1-3


:ref:`Code 3<webapp-gradio-code-how-to-use-tools>` shows how to declare and use these tools.

.. literalinclude:: ./assets/app.py
    :language: python
    :caption: Code 3: How to use tools
    :name: webapp-gradio-code-how-to-use-tools
    :lines: 82-83

Once all the tools are defined, you are ready to create your agent.
An agent is based on a prompt and uses some tools and an LLM.
:ref:`Code 4<webapp-gradio-code-declaring-agent>` is about creating an *agent* and the associated *agent executor*.

.. literalinclude:: ./assets/app.py
    :language: python
    :caption: Code 4: Declaring an agent
    :name: webapp-gradio-code-declaring-agent
    :lines: 85-110

.. _webapp-gradio-agent-creating-the-gradio-application:

Creating the Gradio application
###############################

You now have a working agent; let's build the Gradio application.
This first version has an input Textbox for entering a customer ID and displays the result in an output Textbox.
Thus, the code is straightforward.
You need to connect your agent to the Gradio framework, as shown in :ref:`Code 5<webapp-gradio-code-first-version>`.

.. literalinclude:: ./assets/app.py
    :language: python
    :caption: Code 5: First version of the application
    :name: webapp-gradio-code-first-version
    :lines: 112-127,180

.. literalinclude:: ./assets/app.py
    :language: python
    :lines: 182-187
    :dedent: 4

.. literalinclude:: ./assets/app.py
    :language: python
    :lines: 205-214


This will lead to an application like the one shown in :ref:`Figure 3<webapp-gradio-agent-application-first-version>`.

.. _webapp-gradio-agent-application-first-version:

.. figure:: ./assets/webapp-gradio-agent-application-first-version.png
    :align: center
    :class: with-shadow image-popup
    :alt: Figure 3: First version of the web app.

    Figure 3: First version of the web app.


Going further
#############

You have an application that takes a customer ID as input and displays the result.
However, the result is displayed only when the agent has it, and you don't see the agent's actions to obtain it.
The second version of the application (:ref:`Code 6<webapp-gradio-code-second-version>`) displays the process as it goes along.

.. literalinclude:: ./assets/app.py
    :language: python
    :caption: Code 6: Second version of the application
    :name: webapp-gradio-code-second-version
    :lines: 129-149,180

.. literalinclude:: ./assets/app.py
    :language: python
    :lines: 189-193
    :dedent: 4

.. literalinclude:: ./assets/app.py
    :language: python
    :lines: 205-214

:ref:`Code 7<webapp-gradio-code-final-version>` shows how to show how the agent is acting more comprehensively.
:ref:`Figure 5<webapp-gradio-agent-application-final>` shows the result of this code.

.. literalinclude:: ./assets/app.py
    :language: python
    :caption: Code 7: Final version of the application
    :name: webapp-gradio-code-final-version
    :lines: 151-180

.. literalinclude:: ./assets/app.py
    :language: python
    :lines: 196-204
    :dedent: 4

.. literalinclude:: ./assets/app.py
    :language: python
    :lines: 205-214


.. _webapp-gradio-agent-application-final:

.. figure:: ./assets/webapp-gradio-agent-application-final.png
    :align: center
    :class: with-shadow image-popup
    :alt: Figure 4: Final version.
    
    Figure 4: Final version.
    

If you want to test different usage of an LLM, follow the steps:

* Use the :meth:`~dataikuapi.dss.project.DSSProject.list_llms()` method (like shown :ref:`here<ce/llm-mesh/get-llm-id>`).
* Store the result in a list.
* Use this list as a dropdown.
* Create a new agent each time the user changes the input.

There are many other ways to improve this application, but you now have enough knowledge to adapt it to your needs.

Here are the complete versions of the code presented in this tutorial:

.. dropdown:: :download:`app.py<./assets/app.py>`

    .. literalinclude:: ./assets/app.py
        :language: python
