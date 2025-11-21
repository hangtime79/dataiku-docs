Models ensembling
##################

You can ensemble prediction models in DSS using various ensembling methods.

In the analysis results page, select several models, and click Actions > Create ensemble model.

Limitations
============

* Only models trained with the same preprocessing settings can be ensembled.
* It is not possible to ensemble models with different time ordering or weight parameters.
* It is not possible to ensemble models trained using K-Fold cross-test.
* It is not possible to ensemble models trained with vector or image features.
* It is not possible to ensemble partitioned models.
* It is not possible to ensemble computer vision models.
* After deployment as a saved model, it is not possible to retrain an ensemble model on the automation node.
* After deployment as a saved model, it is not possible to retrain an ensemble model if the original models have been removed from the analysis screen.

.. todo::

	* Detail the concepts
	* Detail ensembling methods
