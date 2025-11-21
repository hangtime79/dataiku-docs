Chat UI
#######

Agent Hub
----------

AI chatbots have become indispensable tools for automating repetitive tasks, delivering instant support, and streamlining collaboration. 

:doc:`Agent Hub</agents/agent-hub>` is the central portal for organizations to distribute enterprise-level agents, manage access, and empower users to build their own custom agents.

    .. image:: /agents/img/AgentHubLibrary.png


Other Chat UIs
----------------


In addition to Agent Hub, Dataiku also includes two fully-featured chatbot user interfaces, allowing you to expose rich chatbots to your users. They handle security, tracing, user preferences, history, and are customizable.

* :doc:`Answers</generative-ai/chat-ui/answers>` is a full-featured chat user interface for creating chatbots based on your internal knowledge and data.

    .. image:: ../img/answers-overview.png

* :doc:`Agent Connect</generative-ai/chat-ui/agent-connect>` is an advanced multi-agent chat interface that provides unified access to multiple generative AI services, including:

    * :doc:`Answers instances </generative-ai/chat-ui/answers>`

    * :doc:`Agents</agents/index>`

    .. image:: ../img/agent-connect-overview.png


.. warning::
	An :doc:`Agent Connect</generative-ai/chat-ui/agent-connect>` service is not itself an agent but instead an agent router, as it routes the user requests towards the relevant generative AI services. 
	When several services are selected to fulfill a user request, Agent Connect combines their responses to generate a final answer.

.. note::
	You can read the :doc:`case study</generative-ai/chat-ui/case-study>` to better understand how you can leverage both :doc:`Answers </generative-ai/chat-ui/answers>` and :doc:`Agent Connect</generative-ai/chat-ui/agent-connect>`.


Going further [Answers & Agent Connect]
---------------------------------------

.. toctree::
	:maxdepth: 2

	answers
	agent-connect
	case-study