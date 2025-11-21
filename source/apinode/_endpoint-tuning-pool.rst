Without API Deployer
----------------------

.. note::

	This method is not available on Dataiku Cloud.

You can configure the parallelism parameters for the endpoint by creating a JSON file in the
``config/services`` folder in the API node's data directory.

.. code-block:: bash

    mkdir -p config/services/<SERVICE_ID>


Then create or edit the ``config/services/<SERVICE_ID>/<ENDPOINT_ID>.json`` file

This file must have the following structure and be valid JSON:

.. code-block:: json

    {
        "pool" : {
            "floor" : 1,
            "ceil" : 8,
            "cruise": 2,
            "queue" : 16,
            "timeout" : 10000
        }
    }

Those parameters are all positive integers:

* ``floor`` `(default: 1)`: Minimum number of pipelines. Those are allocated as
  soon as the endpoint is loaded.

* ``ceil`` `(default: 8)`: Maximum number of allocated pipelines at any given
  time. Additional requests will be queued. ``ceil ≥ floor``

* ``cruise`` `(default: 2)`: The "nominal" number of allocated pipelines. When
  more requests come in, more pipelines may be allocated up to ``ceil``. But
  when all pending requests have been completed, the number of pipeline may go
  down to ``cruise``. ``floor ≤ cruise ≤ ceil``

* ``queue`` `(default: 16)`: The number of requests that will be queued when
  ``ceil`` pipelines are already allocated and busy. The queue is fair: first
  received request will be handled first.

* ``timeout`` `(default: 10000)`: Time, in milliseconds, that a request may
  spend in queue wating for a free pipeline before being rejected.


Creating a new pipeline is an expensive operation, so you should aim ``cruise`` around the expected maximal nominal query load.

With API Deployer
------------------

You can configure the parallelism parameters for the endpoint in the Deployment settings, in the "Endpoints tuning" setting.

* Go to the Deployment Settings > Endpoints tuning
* Add a tuning block for your endpoint by entering your endpoint id and click Add
* Configure the parameters

Those parameters are all positive integers:

* ``Pooling min pipelines`` `(default: 1)`: Minimum number of pipelines. Those are allocated as
  soon as the endpoint is loaded.

* ``Pooling max pipelines`` `(default: 8)`: Maximum number of allocated pipelines at any given
  time. Additional requests will be queued. ``max pipelines ≥ min pipelines``

* ``Pooling cruise pipelines`` `(default: 2)`: The "nominal" number of allocated pipelines. When
  more requests come in, more pipelines may be allocated up to ``max pipelines``. But
  when all pending requests have been completed, the number of pipeline may go
  down to ``cruise pipelines``. ``min pipelines ≤ cruise pipelines ≤ ceil pipelines``

* ``Pooling queue length`` `(default: 16)`: The number of requests that will be queued when
  ``max pipelines`` pipelines are already allocated and busy. The queue is fair: first
  received request will be handled first.

* ``Queue timeout`` `(default: 10000)`: Time, in milliseconds, that a request may
  spend in queue waiting for a free pipeline before being rejected.

Creating a new pipeline is an expensive operation, so you should aim ``cruise pipelines`` around the expected maximal nominal query load.