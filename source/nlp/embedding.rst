Text Embedding 
###############


.. contents::
	:local:


.. warning::

	You do not need this for RAG purposes. Please see :doc:`/generative-ai/knowledge/index` instead


Text Embedding refers to the process of computing a numerical representation of a piece of text (often a sentence), that can then be used as a feature vector for Machine Learning.

Text Embeddings are computed using large-scale embedding models that generate vectors that are close for related pieces of text.

Native embedding in Visual Machine Learning
============================================

Text embedding is a native feature handling option for text features in Visual ML. Please see :doc:`/machine-learning/features-handling/text` for more information. With this method, you can benefit for high quality extraction from text features without any specific configuration or work

Explicit embedding
====================

Alternatively, you can also use the "Sentence Embedding" plugin. This plugin provides a recipe that allows you to retrieve the text embeddings directly as a vector column. This can be used for further customized processing in code. This can also be used for `similarity search <https://www.dataiku.com/product/plugins/similarity-search/>`_

This feature is only available in English.

.. note::

	This capability is provided by the "sentence-embedding" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`

.. warning::

	You do not need this plugin for RAG purposes, nor for having text features in VisualML

The plugin contains:

* A macro that allows you to download pre-trained word embeddings from various models: Word2vec, GloVe, FastText or ELMo.
* A recipe that allows you to use these vectors to compute sentence embeddings. This recipe relies on one of two possible aggregation methods:

  * Simple Average: Averages the word embeddings of a text to get its sentence embedding.
  * SIF embedding: Computes a weighted average of word embeddings, followed by the removal of their first principal component. For more information about SIF, you can refer to this paper or this blogpost.

* A second recipe that allows you to compute the distance between texts. It first computes text representations like in the previous recipe. Then it computes their distances using one of the following metrics:
  * Cosine Distance: Computes 1 - cos(x, y) where x and y are the sentences’ word vectors.
  * Euclidean Distance: Equivalent to L2 distance between two vectors.
  * Absolute Distance: Equivalent to L1 distance between two vectors.
  * Earth-Mover Distance: Informally, the minimum cost of turning one word vector into the other. For more details refer to the following Wikipedia article.

Macro: Download pre-trained embeddings
----------------------------------------

This macro downloads the specified model’s pre-trained embeddings (Source) into the specified managed folder (Output folder name) of the flow. If the folder doesn’t exist, it will be auto-created.

Available models:

* Word2vec (English)
* GloVe (English)
* FastText (English & French, selectable via Text language)
* ELMo (English)

Note: Unlike the other models, ELMo produces contextualized word embeddings. This means that the model will process the sentence where a word occurs to produce a context-dependent representation. As a result, ELMo embeddings are better but also slower to compute.

Compute sentence embedding Recipe
----------------------------------

This recipe creates sentence embeddings for the texts of a given column. The sentence embeddings are obtained using pre-trained word embeddings and one of the following two aggregation methods: a simple average aggregation (by default) or a weighted aggregation (so-called SIF embeddings).

* Select the downloaded pre-trained word embeddings, your dataset with the column(s) containing your texts, an aggregation method and run the recipe!

Note: For SIF embeddings you can set advanced hyper-parameters such as the model’s smoothing parameter and the number of components to extract.

Note: You can also use your own custom word embeddings. To do that, you will need to create a managed folder and put the embeddings in a text file where each line corresponds to a different word embedding in the following format: word emb1 emb2 emb3 ... embN where emb are the embedding values. For example, if the word dataiku has a word vector [0.2, 1.2, 1, -0.6] then its corresponding line in the text file should be: dataiku 0.2 1.2 1 -0.6.

Compute Sentence Similarity Recipe
------------------------------------

This recipe takes two text columns and computes their distance. The distance is based on sentence vectors computed using pre-trained word embeddings that are compared using one of three available metrics: cosine distance (default), euclidian distance (L2), absolute distance (L1) or earth-mover distance.

Using this recipe is similar to using the “Compute sentence embeddings” recipe. The only differences are that you will now choose exactly two text columns and you will have the option to choose a distance metric from the list of available distances.

References
-----------

SIF references:
Sanjeev Arora, Yingyu Liang and Tengyu Ma, A Simple but Tough-to-Beat Baseline for Sentence Embeddings

Word2vec references:
Tomas Mikolov, Kai Chen, Greg Corrado, and Jeffrey Dean. Efficient Estimation of Word Representations in Vector Space. In Proceedings of Workshop at ICLR, 2013.

Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, and Jeffrey Dean. Distributed Representations of Words and Phrases and their Compositionality. In Proceedings of NIPS, 2013.

Tomas Mikolov, Wen-tau Yih, and Geoffrey Zweig. Linguistic Regularities in Continuous Space Word Representations. In Proceedings of NAACL HLT, 2013.

GloVe references:
Jeffrey Pennington, Richard Socher, and Christopher D. Manning. 2014. GloVe: Global Vectors for Word Representation.

FastText references:
P. Bojanowski, E. Grave, A. Joulin, T. Mikolov, Enriching Word Vectors with Subword Information

ELMo references:
Matthew E. Peters, Mark Neumann, Mohit Iyyer, Matt Gardner,
Christopher Clark, Kenton Lee, Luke Zettlemoyer. Deep contextualized word representations NAACL 2018.