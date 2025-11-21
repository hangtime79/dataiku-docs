Creating a plugin Processor component
**************************************

In this tutorial, you will learn how to create your own plugins by developing a preparation processor (or Prepare recipe step) that hides certain words in a dataset's column.
   
Prerequisites
==============
This lesson assumes that you have a:

- A basic understanding of coding in Dataiku. 
- A Dataiku version 12.0 or above (the `free edition <https://www.dataiku.com/product/plans-and-features/>`_ is compatible.) 
- A Python code environment that includes the ``matplotlib`` package. 
  
  .. note::
    
   This tutorial was tested using a **Python 3.9** code environment, other Python versions may be compatible.


Creating a plugin preparation processor component
=================================================

A preparation processor provides a visual user interface for implementing a Python function as a *Prepare* recipe step. 
The processor will hide certain words that appear in a dataset's column.

.. tip::
   Preparation processors work on rows independently; therefore, only Python functions that perform row implementations are valid. 
   If your Python function performs column aggregates, for example, it won't be a proper preparation processor.

   Also, preparation in Dataiku should be interactive. Thus, the code that is executed should be fast.

To create a plugin preparation processor component:

1. From the Application menu, select **Plugins**.
2. Select **Add Plugin > Write your own**.
3. Give the new plugin a name like ``hiding-words-processor`` and click **Create**.
4. Click **+Create Your First Component** and select **Preparation Processor**.
5. Give the new component an identifier and click **Add**.

The preparation processor plugin component comprises two files: a configuration file (``processor.json``) and a code file (``processor.py``).
They are composed of code samples that need to be modified. 

Editing the JSON descriptor
---------------------------


The JSON file contains the metadata (``"meta"``) and the parameters (``"params"``) to be described by the user for the plugin.
For our example, the JSON can be modified as follows:

.. literalinclude:: ./assets/processor.json
    :language: json
    :caption: ``processor.json``
    :lines: 1-44
    :name: tutorial_plugins_processor_json


For more information on the customizations in the JSON file, see :doc:`Component: Preparation Processor <refdoc:plugins/reference/preparation>` in the reference documentation.

Editing the Python code
-----------------------

We want the processor to hide certain words that appear in our dataset in a case-insensitive manner.
To do that, we can use a python functions that take each rows of the dataset as a parameter and returns the modified row.

.. literalinclude:: ./assets/processor.py
    :language: python
    :caption: ``processor.py``
    :lines: 1-17
    :name: tutorial_plugins_processor_py



Test the preparation processor 
--------------------------------
You can test the processor component from the Prepare recipe in the Flow.

1. Refresh the Flow of your project.
2. Open the Prepare recipe and click **+Add a New Step**.
3. Begin to search for ``Hide text`` and select **Hide text**.
4. Configure the processor as follows:

   - **Output column**: ``Hidden_Text_Column``
   - **Input column**: ``Column_With_Text_To_Hide``

5. Scroll across the Preview page to view the output column *Hidden_Text_Column* with text hidden (that is, replaced with "\****").
6. **Run** the Prepare recipe and **Update Schema**.

What's next?
==============================

In this lesson, you have learned how to create a custom preparation for recipes.
You can check other :doc:`tutorials on plugins <./../../../plugins/index>` to see how you can mutualize more components.

.. dropdown:: recipe.json

    .. literalinclude:: ./assets/processor.json
        :language: json

.. dropdown:: recipe.py

    .. literalinclude:: ./assets/processor.py
        :language: python


