Code Agents
#############

Code Agents allow to build an agent in a controllable and customizable manner.

As the builder of a Code Agent, you need to write the code containing your Agent's logic.

Dataiku handles the plumbing and management of your agent:

* Spinning your code up and down
* Handling multiple parallel requests and scaling up and down
* Auditing and securing calls to the agents
* Running your agent in containers
* ...

Your code can leverage our extensive LangChain integration and, of course,
all :doc:`Dataiku Managed Tools <tools/index>` to increase productivity of writing the agent.

You can find :doc:`code samples<devguide:concepts-and-examples/agents>`
and :doc:`tutorials<devguide:tutorials/genai/agents-and-tools/index>` in the developer guide.

Dataiku also provides an interactive test environment for your Agent.

To create a Code Agent, from the Flow, click "+Other > Generative AI > Code Agent". Several code samples are provided to help you quickly start.

Requirements
==============

In order to write your Code Agent, you need a Python 3.10 or above code env. Create the code env, and make sure it's selected in the Advanced Settings of the agent.

While no packages are strictly required, you'll often want to use LangChain and/or LangGraph, and should add them to the code env if needed.


What does the Code do
======================

When writing a Code Agent, your task is to implement a class like this:

.. code-block:: python

    import dataiku
    from dataiku.llm.python import BaseLLM

    class MyLLM(BaseLLM):

        def process(self, query, settings, trace):

            # Query is a Dataiku LLM Mesh completion query. It contains "messages", with "content".
            # For example, to get the last message's content:
            prompt = query["messages"][-1]["content"]

            # The agent must then build a response, which notably contains "text"

            resp_text = "I am a starter agent, and you wrote: %s. How are you?" % prompt
            return {"text": resp_text}


Of course, most agents will actually leverage LLMs, through the LLM Mesh. For example:


.. code-block:: python

            # This is an example, replace by your own
            LLM_ID="vertex:myvertexconnection:gemini-1.5-pro"

            llm = dataiku.api_client().get_default_project().get_llm(LLM_ID)
            llm_resp = llm.new_completion() \
                        .with_message("The user wrote this. What do you think about this question, without answering it?", "system") \
                        .with_message(prompt) \
                        .execute()
            
            resp_text = "The LLM thinks this about your question: %s" % (llm_resp.text)
            return {"text": resp_text}

Using tools
============

Your code may choose to use Dataiku-managed tools, using their API

Streaming
==========

Streaming responses is an important part of providing better experience to users, especially when the Agent is meant to be used in a Chat UI. The code samples when creating a Code Agent show how to stream answers, either directly, or through the LangChain / LangGraph integration.
