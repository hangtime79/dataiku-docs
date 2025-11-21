Publishing Datasets to a Data Collection
========================================

Publishing a dataset to a Data Collection can be done from:

- the right panel of the dataset (from the flow, the dataset page...)

- the Data Collection itself (blue "Add Dataset" button)

While adding the dataset, if it is not already readable, the user can add "Allow read" or "Allow discover" object authorization in order to improve its discoverability. See :doc:`related documentation</data-catalog/data-collections/permissions-and-dataset-visibility>` for details.

To be permitted to publish datasets to a Data Collection, a user must have all of the following authorizations:

- "Publish to Data Collections" global group authorization, granted by an instance admin

- "Publish to Data Collections" project-level authorization for the project that contains the dataset, granted by a project admin

- "Contributor" or "Admin " role on the Data Collection, granted by a Data Collection admin

Removing Datasets from a Data Collection
========================================

Any Data Collection member with the "Contributor" or "Admin " role may remove datasets from the collection.

This can be done using the "Remove" button in the right-panel of the Data Collection page, when the dataset is selected. The dataset is removed from the Data Collection, but unaffected elsewhere (in its source project, or any workspace it may be published on, for example).

.. note ::

    If the user doesn't have the "Publish to Data Collections" global group authorization or the "Publish to Data Collections" project-level authorization for the project that contains the dataset, they would not be able to revert the dataset removal.
