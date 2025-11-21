Adding traces to your Agent
****************************

.. meta::
  :description: Description

Once you have created an agent, for example,
after following the :doc:`/tutorials/genai/agents-and-tools/code-agent/index` tutorial
or the :doc:`/tutorials/plugins/agent/generality/index` tutorial,
it is essential to trace its behavior to understand better what happened and to ease debugging.

Prerequisites
#############

- Dataiku >= 13.4
- An OpenAI connection
- Python >= 3.10

Additionally, if you want to start from one of the tutorials mentioned, you will need the corresponding prerequisites,
as described in each tutorial.

Introduction
############

Adding traces to your Agent's code can help you understand the path your Agent has taken.
It will be a tool to diagnose the potential issues that may occur.
It's also a way to analyze each step's performance, helping to identify the steps to focus your efforts on and allowing performance improvements.

Adding traces to your Code Agent
################################

At the end of the :doc:`/tutorials/genai/agents-and-tools/code-agent/index` tutorial, you end up with the following code.
Let's see how the traces can be tailored to suit your needs.

.. dropdown:: code-custom.py

    .. literalinclude:: /tutorials/genai/agents-and-tools/code-agent/assets/code-custom.py
        :language: python
        :caption: Code 1: Using Custom Tools
        :name: tutorials-genai-techniques-and-tools-code-agents-illustrate-tracing

The workflow of traces starts within the ``process`` function in the ``MyLLM`` class.

.. code-block:: python
    :emphasize-lines: 5

    class MyLLM(BaseLLM):
        def __init__(self):
            pass

        def process(self, query, settings, trace):

The ``trace`` object will then be used to add a ``subspan`` to the generated traces.

.. code-block:: python
    :emphasize-lines: 1,6

    with trace.subspan("Invoke LLM with tools") as subspan:
        ai_msg = llm_with_tools.invoke(messages)

    tool_messages = []

    with trace.subspan("Call the tools") as tools_subspan:

You can organize the traces by naming each step you want to identify in your workflow.

You can also enrich a ``span`` with specific data.

.. code-block:: python
    :emphasize-lines: 2-3

    with trace.subspan("Call a tool") as tool_subspan:
        tool_subspan.attributes["tool_name"] = tool_call["name"]
        tool_subspan.attributes["tool_args"] = tool_call["args"]

The global structure of the span is as described below:

.. code-block:: python

    {
      "type": "span",
      "begin": "",
      "end": "",
      "duration": ,
      "name": "",
      "children": [],
      "attributes": {},
      "inputs": {},
      "outputs": {}
    }

You can fill out this dict with all the metadata required for your specific needs.

* The fields ``begin`` and ``end`` are timestamps completed by the ``duration`` field.
* The ``name`` field is the one specified when calling ``trace.subspan``.
* The ``children`` field represents the array of subspan for this span.
* The attributes field is the one we modified to trace the name and arguments of a tool call.
* The last files are the ``inputs`` and ``outputs`` used in the case of LLM calls.

Last, every LLM Mesh call has a trace, which you can append to a span.
You can build your own trace hierarchy, as shown below:

.. code-block:: python

    with trace.subspan("Calling a LLM") as subspan:

       llm = dataiku.api_client().get_default_project().get_llm(<your LLM id>)
       resp = llm.new_completion().with_message("this is a prompt").execute()

       subspan.append_trace(resp.trace)


LangChain-compatible traces
###############################

| For the specific case of a LangChain-based agent, you can easily write a LangChain-compatible trace in your Dataiku trace object.
| Instantiate the ``LangchainToDKUTracer`` class and use it in each LangChain runnable you wish to track.
| Let's illustrate this with an example from the :doc:`/tutorials/plugins/agent/generality/index` tutorial.
| You end up with the following code.

.. dropdown:: agent.py

    .. literalinclude:: /tutorials/plugins/agent/generality/assets/agent.py
        :language: python

The tracing workflow starts with the ``aprocess_stream`` function in the ``MyLLM`` class.

.. code-block:: python
    :emphasize-lines: 5

    class MyLLM(BaseLLM):
        def __init__(self):
            pass

        async def aprocess_stream(self, query, settings, trace):

You use the ``trace`` object to create a ``LangchainToDKUTracer`` object.
You can then register this tracer object on all callbacks in the configuration of the ``AgentExecutor`` asynchronous events.

.. code-block:: python
    :emphasize-lines: 4,8

    async def aprocess_stream(self, query, settings, trace):
        prompt = query["messages"][0]["content"]

        tracer = LangchainToDKUTracer(dku_trace=trace)
        agent_executor = AgentExecutor(agent=self.agent, tools=tools)

        async for event in agent_executor.astream_events({"input": prompt}, version="v2",
                                                         config={"callbacks": [tracer]}):

This will collect all the traces generated by the different calls made by your LangChain-based Agent.

Wrapping up
###########

With this tutorial, you now have the tools at hand to architect the traces you need:

- Create and organize your own trace with ``trace.subspan``
- Build your trace hierarchy with ``span.append_trace``
- For LangChain agents, easily log the execution with a LangChain-compatible tracer, using ``LangchainToDKUTracer``

.. seealso::
    | More information on how Dataiku handles tracing is available in the :doc:`refdoc:agents/tracing` chapter of the documentation.
