NLP using AWS APIs
######################

.. contents::
	:local:

Dataiku can leverage multiple AWS APIs to provide various NLP capabilities

AWS Transcribe
===============

The AWS Transcribe integration provides speech-to-text extraction in `40 languages <https://docs.aws.amazon.com/transcribe/latest/dg/supported-languages.html>`_ 

.. note::

	This capability is provided by the "Amazon Transcribe" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`


Please see our `Plugin documentation page <https://www.dataiku.com/product/plugins/amazon-transcribe/>`__ for more details

AWS Comprehend
===============

The AWS Comprehend integration provides:

* :doc:`language-detection` in `100 languages <https://docs.aws.amazon.com/comprehend/latest/dg/how-languages.html>`_ 
* :doc:`sentiment-analysis` in `12 languages <https://docs.aws.amazon.com/comprehend/latest/dg/supported-languages.html#supported-languages-feature>`_
* :doc:`named-entities` in `12 languages <https://docs.aws.amazon.com/comprehend/latest/dg/supported-languages.html#supported-languages-feature>`_
* :doc:`key-phrase-extraction` in `12 languages <https://docs.aws.amazon.com/comprehend/latest/dg/supported-languages.html#supported-languages-feature>`_


.. note::

	This capability is provided by the "Amazon Comprehend" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`


 Please see our `Plugin documentation page <https://www.dataiku.com/product/plugins/amazon-comprehend/>`__ for more details


AWS Translation
================


The AWS Translation integration provides translation in `71 languages <https://aws.amazon.com/translate/details/>`_.

.. note::

	This capability is provided by the "Amazon Translation" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`


Please see our `Plugin documentation page <https://www.dataiku.com/product/plugins/nlp-amazon-translation/>`_ for more details
   

AWS Comprehend Medical
=======================


The AWS Comprehend Medical  integration provides Protected Health Information extraction and medical entity recognition in English

.. note::

	This capability is provided by the "Amazon Comprehend Medical" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`

.. warning::

	Costs for the AWS Comprehend Medical API are significantly higher than other APIs


Please see our `Plugin documentation page <https://www.dataiku.com/product/plugins/amazon-comprehend-medical/>`__ for more details
