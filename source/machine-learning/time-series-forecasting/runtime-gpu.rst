Runtime and GPU support
#######################

The training/scoring of time series forecasting deep learning models can be run on either a CPU or **one** GPU. Training on a GPU is usually much faster.

Code environment
================

Time series forecasting in DSS uses specific Python libraries (such as GluonTS and Torch) that are not shipped with the DSS built-in Python environment.

Therefore, before training your first time series forecasting deep learning model, you must create a code environment with the required packages. See :doc:`/code-envs/index` for more information about code environments.

You can select the "Visual Machine Learning and Timeseries Forecasting (GPU)" package preset in the "Packages to install" section of the code environment settings.

.. warning::

  To train or score a time series forecasting model on GPU, DSS needs:

  * At least one CUDA compatible NVIDIA GPU.
  * The GPU drivers installed, with CUDA 12.2 or more recent.
  * A compatible version of NVIDIA NCCL installed, at least 2.4.2.
  * A compatible version of NVIDIA CuDNN installed, at least 7.5.1.


.. note::

  You might need to set the ``LD_LIBRARY_PATH`` environment variable in your ``DATADIR/bin/env-site.sh`` to point towards you CUDA library folder
  (e.g. ``export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH``)

Selection of GPU
================

Once the proper environment is set up, you can create a time series forecasting modeling task.
DSS will look for an environment that has the required packages and select it by default.

If the DSS instance has access to GPU(s) you can then choose **one** of them to train the model.

.. image:: img/gpu-selection.png

For containerized execution you can only select the number of GPUs (at most **one** for time series forecasting).

If a model trained on a GPU code environment is deployed as a service endpoint on an API node, the endpoint will require access to a GPU on the API node, with the same CUDA version,
and will automatically use GPU resources.
