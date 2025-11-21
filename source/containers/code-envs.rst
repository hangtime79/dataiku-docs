Using code envs with containerized execution
############################################

Container-based execution is compatible with managed code environments for:

* Python recipes
* R recipes
* Custom in-memory machine learning models
* Deep learning models
* Python notebooks
* R notebooks

To make a code environment usable for containerized execution, you must select the containerized execution
configuration(s) for which the code environment Docker image must be available.
This setting is configured in the "Containerized execution" tab of the code env settings.

.. warning::

  Container-based execution is not compatible with:

  * non-managed code environments, i.e. those that have deployment type
    "Non-managed path" or "Named external Conda env"
  * custom python interpreter from ``PATH``
  * additional ``PYTHONPATH`` entries.
  * custom packages manually added to DSS' builtin environment

.. _code-env-resources-containerized:

Code environment resources directory
====================================

:ref:`Managed code environment resources directory <code-env-resources-directory>` offers 3 modes for containerized execution:

* **Run resources initialization script**: call the resources initialization script from within the container at image build time.
* **Copy resources from local code environment**: copy the resources directory from the local code environment into the docker image (using the COPY docker instruction). This option avoids re-downloading the resources.
* **None**: no resources directory in containerized execution.


Updating code envs
====================

Update a code env from the code env administration page. This causes corresponding Docker images to be built
for the code env (one on top of each base image from the selected container configurations).
Each time you use this code env and one of the selected container configurations to run a recipe or model, then the corresponding Docker image will be used.

.. warning::

	After each upgrade of DSS, you must rebuild all base images and then all code env images.
	You can rebuild code env images by running ``./bin/dssadmin build-container-exec-code-env-images --all``.

	Likewise, adding a new container execution configuration does not automatically rebuild all
	code environments that are set to be available for "All container exec configurations".
