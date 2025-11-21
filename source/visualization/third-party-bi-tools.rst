Third-party BI tools
#####################

In addition to its native charting capabilities, Dataiku supports integrations with several third-party BI tools

.. contents::
	:local:

Tableau
=======

Tableau and Dataiku are complementary solution. In a typical usage scenario:

* Users build workflows in DSS to create complex data transformation pipelines and build machine learning models
* Users can then push the output of these workflows directly to Tableau to be consumed by end users, using its interactive visualization and dashboarding features.

Dataiku can export datasets to a Tableau Server. This makes them directly available for charting in Tableau.

In addition, Dataiku can directly produce a .hyper file for load in Tableau Desktop.

Dataiku can also read .hyper files as datasets.

This capability is provided by the `Tableau Hyper Export plugin <https://www.dataiku.com/product/plugins/tableau-hyper-export/>`_. This plugin is not supported

Microsoft PowerBI
=================

.. warning::

	Microsoft will retire the capability that DSS is using to publish datasets on PowerBI on October 31st, 2027.

	Should you experience any restrictions with the PowerBI API prior to this date, please submit a support ticket through Microsoft's platform. You can find instructions on how to do so `here <https://learn.microsoft.com/en-us/power-bi/support/create-support-ticket>`_.

	Further details are available on the `Microsoft Power BI Blog <https://powerbi.microsoft.com/en-us/blog/announcing-the-retirement-of-real-time-streaming-in-power-bi/>`_ (the comment section is not visible with all browsers and requires to accept cookies) and `Microsoft Learn <https://learn.microsoft.com/en-us/power-bi/connect-data/service-real-time-streaming>`_.

Microsoft Power BI and Dataiku DSS are 2 complementary solutions. In a typical usage scenario:

* Users build workflows in DSS to create complex data transformation pipelines and build machine learning models, possibly relying on other Microsoft technologies (such as Azure Blob Storage, Azure Data Lake Store, Azure HDInsight or SQL Server)
* Users can then push the output of these workflows directly to Power BI to be consumed by end users, using its interactive visualization and dashboarding features.

Dataiku can export datasets to PowerBI. This makes them directly available for charting in PowerBI.

This capability is provided by the `PowerBI plugin <https://www.dataiku.com/product/plugins/microsoft-power-bi-v2>`_. This plugin is not supported.

Qlik
=====

Dataiku can export datasets to Qlik QVX files that can be downloaded by users.

This capability is provided by the `Qlik QVX plugin <https://www.dataiku.com/product/plugins/qlik-qvx>`_. This plugin is not supported.


Microstrategy
===============


Dataiku can export datasets to a MicroStrategy cube.

This capability is provided by the `Microstrategy plugin <https://www.dataiku.com/product/plugins/microstrategy>`_. This plugin is not supported.
