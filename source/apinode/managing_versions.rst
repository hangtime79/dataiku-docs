Managing versions of your endpoint
##################################

.. contents::
	:local:

Updating and activating endpoint versions
==========================================

The page :doc:`first-service-manual` explains how to import a package containing an updated version of your endpoint.

To activate the latest version of your endpoint, use the command:

.. code-block:: bash

	./bin/apinode-admin service-switch-to-newest <SERVICE_ID>


Running multiple versions at once
========================================

Endpoints can serve multiple versions simultaneously, you just need to specify the
probability each version has to be used for scoring a query.

.. note::

	This feature can be used to run some A/B testing of your machine learning
	models.

The API node log of queries will store which version of your
endpoint was used, see :doc:`../operations/logging` for more information about logging.

The mapping of versions/probabilities is defined by a JSON containing entries
with ``generations`` and ``proba`` properties.


.. code-block:: JSON

	{"entries":
		[
			{"generation": "v1",
			 "proba": 0.5
			},
			{"generation": "v2",
			 "proba": 0.5
			}
		]
	}

.. note::
	Probabilities must sum to 1.


The mapping is read from std_in by the command ``service-set-mapping``, example
usage:

.. code-block:: bash

	echo '{"entries":
		[
			{"generation": "v1",
			 "proba": 0.5
			},
			{"generation": "v2",
			 "proba": 0.5
			}
		]
	}' | ./bin/apinode-admin service-set-mapping <SERVICE_ID>


Monitoring version activation
========================================
In order to know which versions of an endpoint are currently served by the API
and their associated probabilities, you can use the command:


.. code-block:: bash

	./bin/apinode-admin service-list-generations <SERVICE_ID>
