Adding Knowledge to LLMs
##########################

While LLMs alone can already handle a large variety of tasks, they only "know" generic things. LLMs usually truly shine when they are augmented with 
your own internal company knowledge.

Retrieval-Augmented Generation, or RAG, is a standard technique used with LLMs, in order to give to standard LLMs the knowledge of your particular business problem.

RAG supposes that you already have a corpus of knowledge. When you query a Retrieval-Augmented LLM, the most relevant elements of your corpus are automatically selected, and are added into the query that is sent to the LLM, so that the LLM can synthesize an answer using that contextual knowledge.


To get started with RAG, you can refer to the following articles in the Knowledge Base:
    
- `Concept | Embed recipe and Retrieval Augmented Generation (RAG) <https://knowledge.dataiku.com/latest/ml-analytics/gen-ai/concept-rag.html>`__
- `Tutorial | Use the Retrieval Augmented Generation (RAG) approach for question-answering <https://knowledge.dataiku.com/latest/ml-analytics/gen-ai/tutorial-question-answering-using-rag-approach.html>`__

.. toctree::

	introduction
	initial-setup
	first-rag
	documents
	vector-stores
	advanced-search
	rag-guardrails
	document-level-security
	graphrag
	../../graph/visual-graph/agent-tool


.. seealso::
    For more information, see also the following articles in the Knowledge Base:

    - `Concept | Embed recipe and Retrieval Augmented Generation (RAG) <https://knowledge.dataiku.com/latest/gen-ai/rag/concept-rag.html>`_
    - `Tutorial | Use the Retrieval Augmented Generation (RAG) approach for question-answering <https://knowledge.dataiku.com/latest/gen-ai/rag/tutorial-rag-embed-dataset.html>`_
