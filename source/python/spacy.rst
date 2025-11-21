Using SpaCy
###########


SpaCy is a Python library for Natural Language Processing (NLP) such as tokenization,
named entity recognition with pre-trained models for several languages.

Documentation for SpaCy is available at https://spacy.io/

Installing SpaCy
================

In a :doc:`code environment </code-envs/index>`, you need to install the ``spacy`` package.

To add a specific pre-trained model, you can add the URL of the pip package for that model,
as specified in the `Installation via pip <https://spacy.io/usage/models#download-pip>`_
page of the SpaCy documentation.

For example for the English model, your code env's Requested Packages could be:

.. code-block:: text

	spacy
	https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.0/en_core_web_sm-2.2.0.tar.gz

.. NOTE: on non-MUS install, can also do, in a notebook: ``spacy.cli.download("en_core_web_sm")``.

See SpaCy's `Models <https://spacy.io/models>`_ page for a list of languages.

Using SpaCy models
==================

In a python notebook or recipe (using the aforementioned code environment), you can then
import ``spacy`` and use ``spacy.load`` with the model package name:

.. code-block:: python

	import spacy
	nlp = spacy.load("en_core_web_sm")
	doc = nlp(u"This is an example sentence.")

