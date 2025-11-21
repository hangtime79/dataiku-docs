Streamlit
#########

Streamlit is a Python library to build interactive webapps for machine learning and data science.

Documentation for Streamlit is available at https://docs.streamlit.io

Create a Code Studio template
=============================

* In "Administration > Code Studios", click **Create Code Studio template** and create a new template named ``streamlit-template``
* In the "Definition" tab, click on **Add a block** and select ``Streamlit``
* In the "Definition" tab, click on **Add a block** and select ``Visual Studio Code``
* Click **Build**

Then in the **Permissions** tab, you can manage which user groups can use the template to create their own Code Studio instances in their projects.

Launch a Code Studio instance
=============================

Once the template is built, in a project with a cluster attached:

* In "Code Studios" click **New Code Studio**
* Select the ``streamlit-template`` Code Studio template, and create a new Code Studio named ``Hello Streamlit``
* Start the Code Studio
* From the **VS Code** tab, you can edit the webapp. The starter file is located at ``code_studio-versioned/streamlit/app.py``. Click on **Sync files with DSS** to persist changes upon Code Studio restart.
* From the **Streamlit** tab, visualize and interact with the webapp. Edits are applied in real-time.

.. image:: img/streamlit.png

Publish your Code Studio as a webapp
====================================

* In "Code Studios", select the ``Hello Streamlit`` Code Studio, and in its action panel, click **Publish**, then **Create**
* Start the webapp and go to the "View" tab

See :doc:`/code-studios/code-studios-as-webapps` for more details about how to configure a webapp from a Code Studio.
