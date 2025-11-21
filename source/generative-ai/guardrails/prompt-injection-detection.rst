Prompt injection detection
##########################

.. note::

    Prompt injection detection is available to customers with the *Advanced LLM Mesh* add-on

Prompt injection detection is an LLM Mesh guardrail aiming to detect "prompt injections" (attempts to override the intended behavior of an LLM) and to block such attempts.

Prompt injection detection can use either:

 * a local prompt injection classifier (from a :doc:`HuggingFace connection <../huggingface-models>`): the specialized model classifies a prompt as possibly dangerous with a given probability, and you set the acceptability threshold
 * or any completion LLM, in LLM-as-a-judge mode: the LLM is tasked with classifying the prompt as "safe" or "unsafe".

LLM-as-a-judge supports multiple detection modes:

 * General detection: the user prompt is inspected for general attempts at subverting the LLM's behavior
 * Detect against the system prompt: the user prompt is inspected for attempts at bypassing the system prompt
 * Write your own prompt: customize the system prompt that is passed to the LLM-as-a-judge. Its user prompt will be the user prompt from the original completion request.

Once a prompt injection detector is set up and enabled for an LLM connection, queries are screened before being submitted. If an injection attempt is detected, the query is rejected.
