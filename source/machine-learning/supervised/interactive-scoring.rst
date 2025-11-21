Interactive scoring
###################

Interactive scoring is a simulator that enables any AI builder or consumer to run “what-if” analyses (i.e., qualitative sensibility analyses) to get a better understanding of what impact changing a given feature value has on the prediction by displaying in real time the resulting prediction and the individual prediction explanations.
For instance in a fraud detection use case, this feature would allow you to see how changing the amount of a transaction affects the predicted probability that it is a fraud.

.. image:: ../img/haiku-ml-interactive-scoring.png

Access the interactive simulator on the **Interactive scoring** tab in the results page of a model. It offers two views:
  - **the compute view** allows you to tweak the input features of your model and see in real time its prediction and the associated explanations.
  - **the comparator view** allows you to compare side-by-side several predictions & explanations

Edit feature values
===================

On the compute view there is a form to edit the feature values.

The default pre-set values are:

- the **medians** in the train set for **numerical** features
- the **modes** in the train set for **categorical** features

For each, you can select between several edit modes (known domain or raw) or choose to ignore the feature, in which case it is not fed to the model.
Feature settings for a given model are saved in your browser for the next time you come back to this page.
If your model has a preparation script, you can choose to define the features as they would be after or before they go through the preparation steps.

From the ``…`` menu, you can copy/paste feature values from other models. Feature values can also be copied from a dataset's explore view by right clicking on a row and choosing "Copy as JSON object".

Comparator
==========

You can add the current feature values and computed results to the comparator. After adding multiple results, open the comparator view to see the predictions and explanations. The content of the comparator is saved in your browser.

.. image:: ../img/haiku-ml-interactive-scoring-compare.png

Note that, if you change the explanation parameters, all the comparator items' explanations will be recomputed with the new parameters.

You can copy the content of the comparator and paste it in another model's comparator to quickly compare those models' behaviors for these specific cases.

The comparator's content can be exported to a Dataset or downloaded as a file.

Publishing on a dashboard
==========================

The interactive scoring interface can be published in a saved model report. In the tile options, the order of the features can be defined under **Advanced options**. Remove some less relevant feature to collapse them at the end under a Details group. Dashboard view will show the features in the specified order.

Limitations
===========

- Interactive scoring is available only for Visual ML models that are trained using the Python or Keras backends.
- Explanations are not supported on Keras or computer vision models.
- Sorting feature by importance is not available for ensembling models, models with custom pre-processing, nor models trained before DSS 8.
