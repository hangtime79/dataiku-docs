Using text features
####################

DSS provides several builtin ways to handle text features, such as Counts vectorization (See :doc:`../features-handling/text` for more details).

However, for Deep Learning algorithms, you may want to use a `Custom preprocessing` to build 2-D or 3-D vectors . In that case, you need to write your own processor (See :doc:`../features-handling/custom`). You can use the `TokenizerProcessor` provided by DSS:

.. code-block:: python

    from dataiku.doctor.deep_learning.preprocessing import TokenizerProcessor

    # Defines a processor that tokenizes a text. It computes a vocabulary on all the corpus.
    # Then, each text is converted to a vector representing the sequence of words, where each
    # element represents the index of the corresponding word in the vocabulary. The result is
    # padded with 0 up to the `max_len` in order for all the vectors to have the same length.

    #   num_words  - maximum number of words in the vocabulary
    #   max_len    - length of each sequence. If the text is longer,
    #                it will be truncated, and if it is shorter, it will be padded
    #                with 0.
    processor = TokenizerProcessor(num_words=10000, max_len=32)

With this example, the output for each text will have a `(32)` shape.  Then, this output is sent to a `textFeature_preprocessed` input, so the corresponding input in the model should look like:

.. code-block:: python

    input_text = Input(shape=(32), name="textFeature_preprocessed")


See `Deep learning for sentiment (text) analysis <https://knowledge.dataiku.com/latest/ml-analytics/nlp/deep-learning-sentiment-analysis/tutorial-index.html>`_  for a step-by-step example of this in practice.
