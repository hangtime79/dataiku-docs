Most Used Datasets
##################

Basics
======

At the bottom of the **Data Collections** home page, you can find a **Most Used Datasets** section containing the most used datasets in your organization’s Dataiku instance.

**Most Used Datasets** are datasets that are considered the most relevant for reuse or publication to data collections, workspaces, or feature stores.

If you have the relevant permissions, you can use a most used dataset in your own projects or publish it into a Workspace, a Data Collection, or the Feature Store.

A dataset is considered most used if it satisfies one of the following conditions:

* It has been shared at least once with another project.

* It is considered a popular dataset.

Popular datasets are dataset that satisfies other more restrictive conditions:

* It has been shared to at least the minimum number of projects set in the settings.

* It has a recent last build date.

* It is used in at least one downstream recipe in a project it is shared with, and that recipe has been run at least once.

Optionally DSS administrators can strengthen these conditions by requiring a popular dataset to be trending, or part of a least one Data Collection.

Settings
========

DSS administrators can enable or disable **Popular Datasets** and tune the settings used for the computation.

To configure Popular Datasets, go to Administration > Settings > Misc.

The following parameters can be configured to drive the conditions a popular dataset must fulfill:

 .. list-table::
   :widths: 35 20 45
   :header-rows: 1

   * - Parameter
     - Default value
     - Description
   * - Max # days since last rebuild
     - 30
     - The maximum number of days since the last build of your dataset. This parameter cannot be set to 0.
   * - Max # days since last used by a new recipe
     - 60
     - The maximum number of days since the dataset has had a new downstream recipe created in a shared project. This parameter cannot be set to 0. This parameter is also used when checking whether a dataset is trending.
   * - Min # shares
     - 3
     - The minimum number of projects a dataset must be shared with to be considered popular (excluding the source project). This parameter cannot be set to 0.
   * - Only from data collections
     - false
     - If true, only consider a dataset as popular if it is part of at least one Data Collection.
   * - Only trending datasets
     - false
     - If true, only consider a dataset as popular if it is trending. **Trending datasets** refer to datasets that exhibit an increasing pattern of new recipe creation over specific temporal windows, determined by analyzing historical usage data.

.. note::

    Popular datasets are not detected across multiple DSS instances.
