Prediction (Supervised ML)
###########################

Prediction (aka supervised machine learning) is used when you have a **target** variable that you want to predict. For instance, you may want to predict the price of apartments in New York City using the size of the apartments, their location and amenities in the building. In this case, the price of the apartments is the **target**, while the size of the apartments, their location and the amenities are the **features** used for prediction.

.. note::

	Our `Machine Learning Basics tutorial <https://knowledge.dataiku.com/latest/ml-analytics/model-design/ml-basics/tutorial-index.html>`_ provides a step-by-step explanation of how to create your first prediction model and deploy it for scoring of new records.

	The rest of this document assumes that you have followed this tutorial.

Use the following steps to quickly start your first prediction model in DSS:

- Go to the Flow for your project
- Click on the dataset you want to use
- Select the *Lab*
- Select *Quick model* then *Prediction*
- Choose your target variable (one of the columns) and *Automated Machine Learning*
- Choose *Quick Prototypes* and click *Create*
- Click *Train*


.. toctree::

  settings
  results
  explanations
  interactive-scoring
  model-exploration
  ml-assertions
  model-fairness-report
  model-error-analysis
  prediction-intervals
  prediction-overrides