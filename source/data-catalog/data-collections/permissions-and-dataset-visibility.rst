Permissions and Dataset Visibility
==================================

A member of a Data Collection may not be authorized to see every dataset published to the Data Collection.
The level of authorization granted and the visibility of datasets depends on the authorization mode applied on the object (see :doc:`Authorized objects </security/authorized-objects>`).

* If the user already has read access to the dataset through another method (read access on the project, on a workspace on which the dataset has been published...), they will be able to see the dataset and all of its details in the Data Collection. Data Collection membership does not grant any additional permission.

* If the user does not already have read access to the dataset but it is an authorized object, the user will also be able to see the dataset in the Data Collection and will be granted some authorization through it.

    * If the dataset has the READ authorization mode, the user is granted access to the dataset in the same way as a workspace or a dashboard-only user (see :doc:`Authorized objects </security/authorized-objects>`). In the Data Collection, they will see the dataset and all details.
    * If the dataset only has the DISCOVER authorization mode, the user will be only granted access to a limited amount of metadata. In the Data Collection, the dataset will appear in the list, but some details will not be shown. Notably, the preview (as well as any access to the dataset content) will be disabled.

* If the user has no other access and the dataset is not an authorized object, they will not be able to see the dataset in the Data Collection. No authorization is granted to the user through the Data Collection.


This table summarizes the details & functionality available for different authorization levels.

.. list-table::
   :header-rows: 1

   * - Info / action
     - Readable dataset
     - Discoverable dataset
   * - Project name
     - Yes
     - Yes
   * - Dataset name
     - Yes
     - Yes
   * - Dataset description
     - Yes
     - Yes
   * - Dataset tags
     - Yes
     - Yes
   * - Data Steward
     - Yes
     - Yes
   * - Dataset status
     - Yes
     - No
   * - Dataset schema
     - Yes
     - No
   * - Usage in other projects
     - Yes
     - No
   * - Quick share
     - If allowed on the dataset
     - No
   * - Request share
     - If allowed on the project
     - If allowed on the project
   * - Export
     - If allowed on the source project
     - No
   * - Preview
     - Yes
     - No
   * - Watch & Star
     - Yes
     - No
