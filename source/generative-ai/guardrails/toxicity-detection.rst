Toxicity detection
##################

Toxicity detection is an LLM Mesh guardrail aiming to detect toxic language in queries & responses, and to block those deemed toxic.

Toxicity detection can use either:

 * OpenAI's moderation API
 * or any local toxicity detection model (from a :doc:`HuggingFace connection </generative-ai/huggingface-models>`): the query or response text is passed to either:

  * a classification model outputting a probability (from 0 to 1, where 0 means safe)
  * or a generic LLM tasked with classifying it as "safe" or "toxic"

.. note::

    Local toxicity detection is available to customers with the *Advanced LLM Mesh* add-on


Once a toxicity detector is set up and enabled, queries are screened before being submitted and responses are screened before saving or displaying the LLM response. 

If toxicity is detected, the request is rejected.
