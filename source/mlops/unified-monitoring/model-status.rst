Understanding Model Status
##########################

To compute the model status of a given Saved Model, Unified Monitoring looks at all Model Evaluation Stores where this Saved Model serves as the input of an Evaluation Recipe.

Then, it looks at all checks of every Model Evaluation Store found.

For every check, Unified Monitoring only takes into account the latest check computation result.

The resulting aggregated model status is computed by taking the worst computation result of the aforementioned checks.

For more details about the Model Evaluation Store, including Metrics and Checks, please see :doc:`../model-evaluations/index`.

.. note::

    
    For "Project" model status, Unified Monitoring will query directly the
    automation node where the project is deployed.

    For "API Endpoint" model status, Unified Monitoring will query the design
    node where the API Package was built. In order for this status to be
    fetched properly, Unified Monitoring needs to query the node using its API
    and so needs the URL and an API key.  If you are on Dataiku Cloud or using
    Fleet Manager, this is setup automatically. If you are using Dataiku
    Custom, an administrator needs to give the details in Administration >
    Settings > Deployer.
