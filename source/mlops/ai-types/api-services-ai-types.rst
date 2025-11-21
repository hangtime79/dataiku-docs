API Service AI Types
####################

Endpoint AI Types
=================


Automatic Assignment
~~~~~~~~~~~~~~~~~~~~

The **ML** AI Type is automatically assigned to prediction and clustering endpoints.


Manual Tagging
~~~~~~~~~~~~~~

It is also possible to manually assign an AI Type to an endpoint by applying the corresponding tag.

The endpoint will automatically receive the AI Type associated with the tag.

.. table::

   ===============  =================
   Tag to Add       Resulting AI Type
   ===============  =================
   ``type-ml``      **ML**
   ``type-llm``     **LLM**
   ``type-agent``   **Agent**
   ===============  =================

Please see :doc:`/collaboration/tags` for more details on objects tagging.


API Service AI Types
====================
The AI types of an API service are determined by the aggregation of the AI types of its individual endpoints.
