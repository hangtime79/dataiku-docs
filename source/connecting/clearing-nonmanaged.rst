Clearing non-managed Datasets
##############################

.. warning::

    Enabling the following option can result in unrecoverable data loss. The option should only be enabled if all input data for the specified connection can be fully cleared and deleted by DSS, without any way to recover the underlying data from DSS. 
    

Non-managed datasets are datasets that point to an existing SQL table or external filesystem store. It's generally expected that non-managed (external) datasets are a source of truth that exist outside of DSS and should not be modified by DSS. By default, users are unable to delete this data in DSS, because deleting this data will result in losing the underlying source data that DSS uses as an input data source.  In the event that the following option is enabled and data is accidentally cleared, **DSS will be unable to recover any non-managed data that has been deleted**. As a result, usually the best workflow is to create a managed dataset based off of your non-managed input dataset, so as not to risk modifying your underlying data source integrity. See :ref:`managed and external datasets<managed-datasets>` for more on the difference between managed and non-managed datasets.

By default, if you attempt to clear data from a non-managed dataset, you'll receive the message:

.. highlight:: none

::

    Unable to clear data for dataset {DATASET}: 
    Clearing external (i.e., non-managed) datasets in connection {CONNECTION} is forbidden. 
    

Under rare circumstances, you might have a workflow that requires clearing non-managed datasets from DSS. If so, you can enable the following option for a given connection by adding this property to the connection under Administration > Connection > Custom Properties > Advanced connection properties:


    ``dku.connection.externalDatasets.allowClear`` : ``true``
