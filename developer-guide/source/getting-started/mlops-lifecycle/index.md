# MLOps lifecycle

```{eval-rst}
.. meta::
    :description: Dataiku streamlines the MLOps lifecycle by providing comprehensive tools for building,
                  deploying, and managing machine learning models efficiently.
                  Its features include experiment tracking, model evaluation, and flexible deployment options,
                  allowing users to leverage both visual and programmatic capabilities throughout the process.
```
Building and deploying machine learning (ML) models is a cornerstone of most data science projects,
and Dataiku provides a comprehensive set of features to ease and speed up these operations.
While the platform offers a wide range of visual capabilities,
it also exposes numerous programmatic elements for anyone who wants to handle their model's lifecycle using code.

## Training

The first step of the machine learning process is to fit a model using training data.
This is an experimental phase during which you can test various combinations of pre-processing, algorithms, and parameters.
Running such trials and logging their results is called **experiment tracking**;
it is implemented natively in Dataiku so that you can use a variety of ML frameworks to train models and log their performance and characteristics.

```{note}
Under the hood, Dataiku uses [MLflow models](https://mlflow.org/docs/latest/models.html) as a standardized format to package models.
```

```{seealso}

* Experiment tracking {doc}`documentation page <refdoc:mlops/experiment-tracking/index>`
* {ref}`Tutorials <machine-learning-tutos/experiment-tracking>` on experiment tracking using different ML frameworks
```

## Import

In some cases, training a model can require much time and computing resources,
so you may prefer to bring in an existing pre-trained model
and perform subsequent operations in the Dataiku platform.

Several features can help speed up this process. You can either:

* Retrieve and cache pre-trained models and embeddings provided by your ML framework of choice using *code environment resources*.
* Bring in model artifacts inside your Flow and store them in managed folders.

You can fine-tune your models using experiment tracking or continue with evaluation and deployment.

```{seealso}

* {ref}`Tutorials <machine-learning-tutos/pretrained-models>` on pre-trained models

```

## Evaluation

Evaluating a model involves computing a set of metrics to reflect how well it performs against a specific *evaluation dataset*. 

In Dataiku, these metrics encompass the model's *predictive power*, *explainability*, and *drift* indicators. 
The values of those metrics are computed in a buildable Flow item called the "evaluation store".
They are accessible either in their raw form using the public API
or visually through a set of rich visualizations embedded in the Dataiku web interface.

```{seealso} 

* Model evaluation stores {doc}`the documentation page <refdoc:mlops/model-evaluations/index>`
  and {doc}`API reference </api-reference/python/model-evaluation-stores>`.
```

## Deployment and scoring

The final step to make a model operational is to *deploy* it on a production infrastructure
where it will be used to *score* incoming data. 
Depending on how the input data is expected to reach the model, Dataiku offers several deployment patterns:

* If the model is meant to be queried via HTTP, 
  Dataiku can package it as a *REST API endpoint*
  and take advantage of cloud-native infrastructures such as Kubernetes to ensure scalability and high-availability.
* For cases where larger *data batches* are expected to be processed and then scored,
  Dataiku allows the deployment of entire projects to production-ready instance types called *Automation nodes*.

Dataiku also offers flexible choices to pilot the deployment process,
which can be executed using the platform's native "Deployer" features
or delegated to an external Continuous Integration/Delivery (CI/CD).

```{note}
For specific cases where models need to be exported outside of Dataiku,
you can generate standalone Python or Java artifacts.
 For more information, see the related {doc}`documentation page <refdoc:machine-learning/models-export>`.
```

```{seealso}

* API services {doc}`documentation page <refdoc:apinode/introduction>`
* [Knowledge Base articles](https://knowledge.dataiku.com/latest/mlops-o16n/ci-cd/index.html) on Dataiku and CI/CD pipelines.
```