Experiment Tracking
###################

Experiment tracking is the process of saving all experiment-related information that you care about for every experiment you run.
This may include parameters, performance metrics, models and any other data relevant to your project.

In Dataiku, this can be done:

* visually, without coding, in the Lab (see :doc:`/machine-learning/supervised/index`)
* when coding, by calling specific APIs to log values of parameters, metrics, ... and then being able to view all of your experiments and associated results.

This section focuses on code-based Experiment Tracking. Code-based Experiment Tracking in DSS uses the `MLflow Tracking <https://www.mlflow.org/docs/2.17.2/tracking.html>`_ API.

.. toctree::
    :maxdepth: 1

    concepts
    tracking
    viewing
    deploying
    extensions
