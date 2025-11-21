Project AI Types
################

Automatic Assignment
====================

Project AI Types are automatically computed based on project contents following the logic:

* **ML**: The project contains one or more machine learning features:

    * A saved model in the Flow

* **LLM**: The project contains one ore more LLM features:

    * A pink object in the Flow
    * An Answers webapp

* **Agent**: The project contains one or more agent features:

    * A visual agent
    * A code agent
    * A plugin agent
    * An Agent Connect or Agent Hub webapp

.. note:: Shared Objects are also considered in the calculation of AI Types.


Manual Tagging
==============
It is also possible to manually assign an AI Type to a project by applying a dedicated tag to certain of its items.

The project will automatically receive the AI Type associated with the tag.

.. table::

   ===============  =================
   Tag to Add       Resulting AI Type
   ===============  =================
   ``type-ml``      **ML**
   ``type-llm``     **LLM**
   ``type-agent``   **Agent**
   ===============  =================

Please see :doc:`/collaboration/tags` for more details on objects tagging.

