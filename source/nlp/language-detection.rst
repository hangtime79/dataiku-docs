Language Detection
##################

.. contents::
	:local:


Language Detection is the process of finding out the language of a piece of text

Dataiku provides multiple language detection capabilities

Native language detection
=========================

The native language detection capability of Dataiku provides language detection in `114 languages <https://github.com/dataiku/dss-plugin-nlp-preparation/blob/ae7691471e1b98aa8c714a97dec963ae5193996b/custom-recipes/nlp-preparation-language-detection/recipe.json#L52>`_ 

It is an offline capability, meaning that it does not leverage a 3rd party API.

.. note::

	This capability is provided by the "Text Preparation" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`

Please see our `Text preparation plugin page <https://www.dataiku.com/product/plugins/nlp-preparation/>`_ for detailed documentation.

AWS Comprehend
===============

The AWS Comprehend integration provides language detection in 100 languages

Please see :doc:`aws-apis` for more details

Azure Cognitive Services
=========================

The Azure  Cognitive Services integration provides language detection in 108 languages

Please see :doc:`azure-apis` for more details