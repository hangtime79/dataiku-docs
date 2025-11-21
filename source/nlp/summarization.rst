Text summarization
##################


.. contents::
	:local:


Text summarization is the process of generating a summary of documents which could be considered as too long.

Extractive summarization extracts the most relevant sentences from the document. Abstractive summarization generates a summary that is not extracted from the original document, but fully generated.

LLM-based summarization
=============================

The :doc:`LLM Mesh </generative-ai/index>` has a native recipe for performing LLM-based summarization. This is usually the most performant option.

Please see our `Tutorial <https://knowledge.dataiku.com/latest/gen-ai/text-processing/tutorial-summarization.html>`_ for detailed information.

Offline Text Summarization
============================

The native text summarization capability of Dataiku provides language-agnostic extractive summarization using open-source models. It is an offline capability, meaning that it does not leverage a 3rd party API.


.. note::

	This capability is provided by the "Text Summarization" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`

This plugin provides a tool for doing automatic text summarization.

It uses extractive summarization methods, which means that the summary will be a number of extracted sentences from the original input text. This can be used for example to turn customer reviews or long reports into shorter texts.

The plugin comes with a single recipe that uses one of three possible models:

* Text Rank[1], which builds a graph of every sentence of the input text, where each text is linked to its most similar sentences, before running the PageRank algorithm to select the most relevant sentences for a summary.
* KL-Sum[2], which summarizes texts by decreasing a KL Divergence criterion. In practice, it selects sentences based on how much they have the same word distribution as the original text.
* LSA[3], which uses Latent Semantic Allocation (LSA) to summarize texts. Basically, this starts by looking for the most important topics of the input text then keeps the sentences that best represent these topics.

How To Use
----------

First, make sure your text data is stored in a dataset, inside a text column, with one row for each document.  Using the recipe is straightforward: select your dataset and the column containing your documents. Then, select a method, set the number of desired sentences and run the recipe!

References
----------

* Rada Mihalcea and Paul Tarau, TextRank: Bringing Order into Texts.

* Aria Haghighi and Lucy Vanderwende, Exploring Content Models for Multi-Document Summarization.

* Josef Steinberger and Karel Ježek, Using Latent Semantic Analysis in Text Summarization and Summary Evaluation.