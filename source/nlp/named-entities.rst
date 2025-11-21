Named Entities Extraction
###########################

.. contents::
	:local:

Named Entities Extraction is the process of recognizing various kinds of entities (persons, cities, diseases, ...) in documents, and tagging each text with the named entities that it contains.

Dataiku provides several named entities extraction capabilities

Native entity extraction
=========================

The native entity extraction capability of Dataiku extracts information about people, dates, places, ...

It is an offline capability, meaning that it does not leverage a 3rd party API.

Extraction is provided in `7 languages <https://github.com/dataiku/dss-plugin-nlp-named-entity-recognition/blob/19a682f579670dec0675b9997fb706dfc4e0dc71/custom-recipes/named-entity-recognition-extract/recipe.json#L61>`_"

.. note::

	This capability is provided by the "Named Entities Recognition" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`

Please see our `Named entity recognition plugin page <https://www.dataiku.com/product/plugins/named-entity-recognition/>`_ for detailed documentation.

AWS Comprehend
===============

The AWS Comprehend integration provides named entity recognition in 12 languages.

Please see :doc:`aws-apis` for more details

Azure Cognitive Services
==========================

The Azure Cognitive Services integration provides named entity recognition in 23 languages.

Please see :doc:`azure-apis` for more details

Google Cloud NLP
==========================

The Google Cloud NLP integration provides named entity recognition in 11 languages.

Please see :doc:`google-apis` for more details
