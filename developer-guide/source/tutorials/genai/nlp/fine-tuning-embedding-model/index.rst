Customizing a Text Embedding Model for RAG Applications
*******************************************************

The embedding model used to create
and retrieve context from a Knowledge Bank is a crucial building block of an RAG pipeline.
Typical embedding models available out-of-the-box today have been pre-trained on generic data,
which can limit their effectiveness for company or domain-specific use cases.
Fine-tuning an embedding model can significantly improve the quality of retrieved documents
and the coherence of generated responses.

In this tutorial, we walk you through customizing a text embedding model for an RAG application
based on highly technical scientific content from fields like Physics, Chemistry, or Biology.

Prerequisites
#############

* Dataiku > 13.3
* The Scientific Question Answering dataset from the Ai2 non-profit AI research institute.
  It is available both on the `HuggingFace Hub <https://huggingface.co/datasets/allenai/sciq>`__ 
  and `Kaggle <https://www.kaggle.com/datasets/thedevastator/sciq-a-dataset-for-science-question-answering/data>`__.
  It contains more than 13k crowdsourced science multiple-choice questions,
  with an additional paragraph that provides supporting evidence for the correct answer.
* The `Sentence Transformers package <https://www.sbert.net/index.html#>`__, maintained today by HuggingFace.
* A :doc:`code environment <refdoc:code-envs/index>` with a Python version 3.10 and with the following packages:
  
  .. code-block:: python

    accelerate>=0.21.0
    sentence-transformers
    datasets
    transformers


Preparing the embedding dataset
###############################

The goal is to fine-tune the model to better find (and retrieve) the appropriate context for a given question.
In other words, we want the model to learn the semantic similarity of highly technical scientific texts. 

For this, we leverage the ``question``
and ``support`` columns of our input dataset as positive pairs of ``(query, context)``. 

We used a *Prepare recipe* to keep only those two columns and renamed them ``anchor`` and ``positive``, respectively.
We also removed the rows where ``positive`` was empty and added an ``_id`` column.
This is an important step since ``sentence_transformers`` expects input datasets
and column names to match the exact format used by the target loss function for your use case. 

We also used a *Split recipe* to create train and test datasets (80/20) randomly. 

.. literalinclude:: ./assets/app.py
    :language: python
    :lines: 1-21

Loading the embedding model
###########################

We use the embedding model
`all-MiniLM-L6-v2 <https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2>`__ from the Hugging Face Hub.
We chose a small model that can be easily fine-tuned, even on a CPU. But you can try any model with the ``sentence-transformers`` tag.

.. literalinclude:: ./assets/app.py
    :language: python
    :lines: 22-23
    :emphasize-lines: 1

Creating an evaluator and evaluating the base model
###################################################

We will use the ``InformationRetrievalEvaluator`` to evaluate the performance of our model.
For a given set of queries, it will retrieve the top-k most similar document out of a corpus (``k = 1`` in our case).
It then computes several metrics based on Mean Reciprocal Rank (MRR), Recall@k, Mean Average Precision (MAP),
and Normalized Discounted Cumulative Gain (NDCG).
NDCG is a good measure of ranking quality, so we'll focus on this one here.

The queries come from our test set,
and we create the corpus for potential retrieval from all "documents" from the train and test split.

.. literalinclude:: ./assets/app.py
    :language: python
    :lines: 25-49

Initializing the loss function
##############################
We employ the standard ``MultipleNegativesRankingLoss``, a well-established method in the field.
This approach necessitates using positive text pairs with an anchor and a corresponding positive sample.

.. literalinclude:: ./assets/app.py
    :language: python
    :lines: 51


Creating a trainer and fine-tuning the embedding model
######################################################

.. literalinclude:: ./assets/app.py
    :language: python
    :lines: 53-101


Here, we don't provide an eval dataset directly; we only provide the evaluator.
It gives us more interesting metrics.
The total number of training steps is:

.. math::
    
    \text{nb_of_epochs} \times \frac{\text{size_of_training_dataset}}{(\text{batch_size} \times \text{gradient_accumulation_steps})}


Evaluating the model against baseline
#####################################

.. literalinclude:: ./assets/app.py
    :language: python
    :lines: 102-

Wrapping up
###########

This tutorial demonstrated how to fine-tune an embedding model on technical,
scientific content using the Sentence Transformers package.
By following the steps to prepare your dataset, load the model, and fine-tune it,
you can enhance document retrieval and response coherence in your Retrieval-Augmented Generation (RAG) applications
for various domain-specific use cases.

Here is the complete code for this tutorial:

.. dropdown:: :download:`app.py<./assets/app.py>`
    :open:

    .. literalinclude:: ./assets/app.py
        :language: python
