Introduction to Agents in Dataiku
#####################################

While the primary task of LLMs is to generate text, this ability to generate text, including structured output (JSON), can be used for building much more advanced applications. In these applications, the LLMs are used in order to achieve tasks beyond "answering based on knowledge", but leveraging data, and even performing actions.

In these applications, the LLM usually acts as a central "brain" that leverages "tools" to do its work. This kind of AI-based application is often called an Agent.

Tools
======

While not mandatory, usually, agents revolve around the concept of Tools. A tool can perform a task, and can describe what kind of input it expects to achieve this task.

Dataiku includes a complete system for managing tools. Dataiku provides many kinds of tools that are built into the platform, and provides extensibility for users to add their own kinds of tools.

The tools managed by Dataiku include security, audit, and most can be configured visually, allowing you to focus on building your Generative AI Application rather than the plumbing of tools.

For more details, see :doc:`tools/index`

Examples of tools include:

* :doc:`Retrieving documents from Knowledge Banks <tools/knowledge-bank-search>`
* :doc:`Searching records in datasets <tools/dataset-lookup>`
* :doc:`Performing Web searches <tools/google-search>`

Types of agents
===============


Visual Agents
-------------

With Dataiku Visual Agents, users can create their own Agent, based on Dataiku-managed Tools, with no coding involved.

A Visual Agent simply defines which tools it uses and optional instructions. The Visual Agent is then fully autonomous to respond to user queries: it chooses on its own which tools to leverage based on the description of the available tools, automatically calls them, and synthesizes the responses.

For more details, see :doc:`visual-agents`

Code Agents
-------------

On the contrary, Code Agents are fully controllable and customizable. As the builder of a Code Agent, you simply need to write the code containing the logic of your Agent.

Your code can leverage our extensive LangChain integration, and of course, leverage all :doc:`Dataiku Managed Tools <tools/index>` in order to increase productivity of writing the agent.

For more details, see :doc:`code-agents`

Other agent kinds
------------------

In addition to the builtin Visual and Code agents, it is possible to leverage Dataiku's extensibility system to define your own kind of agents. A coder can write a plugin to create a new type of agent that can then be leveraged visually by non-coding users.

.. _generative-ai-agent-introduction-using-agents:

Using agents
=============

Once you have defined your agent, it's time to use it.

In Dataiku, every Agent becomes itself a "Virtual LLM" in the LLM Mesh. This means that everywhere you can use the LLM Mesh, you can use an Agent!

This includes:

* In the :doc:`Prompt Studio </generative-ai/prompt-studio>`, for quick interaction with the Agent
* In the Prompt Recipe, for massively applying the Agent to many tasks/cases
* Through Dataiku's Chat UIs, :doc:`Answers and Agent Connect </generative-ai/chat-ui/index>`
* Through the :doc:`LLM Mesh API </generative-ai/api>`

The Agents system is thus fully integrated and unified with the rest of the LLM Mesh. This includes auditing, security and :doc:`Guardrails </generative-ai/guardrails/index>`

