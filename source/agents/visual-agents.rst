Visual Agents
##############

With Dataiku Visual Agents, users can create their own Agent, based on Dataiku-managed Tools, with no coding involved.

A Visual Agent simply defines which tools it uses and optional instructions. The Visual Agent is then fully autonomous to respond to user queries: it chooses on its own which tools to leverage based on the description of the available tools, automatically calls them, and synthesizes the responses.

To create a Visual Agent, from the Flow, click "+Other > Generative AI > Visual Agent".

Dataiku also provides an interactive test environment for your Agent.

At the heart of a Visual Agent, there is a LLM that acts as the central coordinator. You need to choose the LLM that you will use for this purpose. This must be a LLM that supports "tool calling".

The following LLM types in Dataiku support tool calling:

* Anthropic Claude
* Azure OpenAI
* Anthropic Claude via AWS Bedrock
* Mistral AI (on La Plateforme)
* OpenAI
* Vertex Gemini

Once the LLM is chosen, you simply need to choose the tools that the agent will use. Note that you must create the tools before the agent. See :doc:`tools/index` for more details on creating tools.

You can also give additional instructions, for example, to instruct the LLM on what tone to use, what languages to use, what to do when it does not know, etc...

For example, a Customer 360 assistant agent could have several tools:

* A :doc:`Knowledge Bank Search <tools/knowledge-bank-search>` tool to search into past emails with this customer
* A :doc:`Dataset Lookup <tools/dataset-lookup>` tool to search for the latest support tickets from this customer

Sources
========

Many tools are able to provide information about "sources", i.e. providing details of the data and knowledge elements that they used to provide the answer to the agent.

The Visual Agent gathers all the sources used by the tools, and returns them as part of its response. This gives full visibility for end users into how the Visual Agent built its response.

When using the LLM Mesh API, sources are returned in the "sources" field of the completion response. The Dataiku :doc:`Chat UIs </generative-ai/chat-ui/index>` display sources directly to end users.

Context
========

To learn more about what Context is and how tools use it, see :doc:`tools/using-tools`.

Each tool receives a context, and Agents receive a context too. When using a Visual Agent, the Visual Agent passes the entire context it receives to all tools it calls.

When using the LLM Mesh API, the Context is passed as the "context" field of the completion query.