Sentiment Analysis
###################

.. contents::
	:local:

Sentiment Analysis estimates the sentiment polarity (positive/negative) of text data 

Dataiku provides several sentiment analysis capabilities

LLM-based sentiment analysis
=============================

The :doc:`LLM Mesh </generative-ai/index>` has a native recipe for performing LLM-based sentiment analysis. This is usually the most performance option.

Please see our `Tutorial <https://knowledge.dataiku.com/latest/gen-ai/text-processing/tutorial-classification.html>`_ for detailed information.

Offline sentiment analysis
============================

The native sentiment analysis capability provides sentiment analysis in English.

It is an offline capability, meaning that it does not leverage a 3rd party API.

.. note::

	This capability is provided by the "Sentiment analysis" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`


Usage instructions
--------------------

If you have a Dataiku DSS project with a dataset containing text data in English. This text data must be stored in a dataset, inside a text column, with one row for each document.

Navigate to the Flow, click on the + RECIPE button and access the Natural Language Processing menu. If your dataset is selected, you can directly find the plugin on the right panel, and click "Sentiment analysis"


* The Text column parameter lets you choose the column of your input dataset containing text data.

* Choose your Sentiment scale.

  * Either binary (0 = negative, 1 = positive) or 1 to 5 (1 = highly negative, 5 = highly positive).
  * Default is binary.

* Choose whether to Output predictions as numbers and/or Output predictions as categories.

  * These parameters depend on the chosen Sentiment scale.
  * Default is yes to both.

* Choose whether to Output confidence scores for the predicted sentiment polarity.

  * Confidence scores are from 0 to 1.
  * Default is false.

Output dataset will be a copy of the input dataset with additional columns on predicted sentiment polarity


AWS Comprehend
===============

The AWS Comprehend integration provides sentiment analysis in 12 languages.

Please see :doc:`aws-apis` for more details

Azure Cognitive Services
============================

The Azure Cognitive Services integration provides sentiment analysis in 13 languages.

Please see :doc:`azure-apis` for more details

Google Cloud NLP
==================

The Google Cloud NLP integration provides sentiment analysis in 16 languages.

Please see :doc:`google-apis` for more details