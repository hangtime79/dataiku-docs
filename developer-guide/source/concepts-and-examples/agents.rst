Agents
******

..
  this code samples has been verified on DSS: 14.2.0
  Date of check: 11/09/2025

| For more details on the Agents, please refer to our documentation: :doc:`refdoc:agents/index`.
| For more details on the LLM Mesh, please refer to our documentation :doc:`refdoc:generative-ai/introduction`.
| If you want more information about the LLM Mesh API, please refer to :doc:`./llm-mesh`.

.. admonition:: Tutorials

    You can find tutorials on this subject in the Developer Guide: :doc:`/tutorials/genai/agents-and-tools/index`.

.. note::
    Once you have a ``DKUChatModel``, obtained by :meth:`~dataikuapi.dss.llm.DSSLLM.as_langchain_chat_model`,
    you can use the langchain methods (like ``invoke``, ``stream``, etc.)

.. tip::
    In the code provided on this page, you will need to provide ID of other elements.
    You will find how to :ref:`list your LLM<ce/llm-mesh/get-llm-id>` , :ref:`list your Knowledge Bank<llm-mesh-get-kbs>`
    or :ref:`list your Agent Tools<ce/agents/agent-tools/listing>` in dedicated pages.

Listing your agents
===================

The following code lists all the Agents and their IDs,
which you can reuse in the code samples listed later on this page.

.. code-block:: python
    :name: ce/agents/list_your_agents
    :caption: How to retrieve an Agent's ID

    import dataiku

    client = dataiku.api_client()
    project = client.get_default_project()
    llm_list = project.list_llms()
    for llm in llm_list:
        if 'agent:' in llm.id:
            print(f"- {llm.description} (id: {llm.id})")


.. _ce_llm_agent_using_your_agent:

Using your agent
================

.. tabs::
    .. group-tab:: Native DSSLLM

        Using the native :class:`~dataikuapi.dss.llm.DSSLLM` completion, for more information,
        refer to :ref:`ce-llm-mesh-native-llm-completion-on-queries`:

        .. code-block:: python
            :name: ce/agents/native-dssllm/using-agent
            :caption: Using your agent

            import dataiku

            AGENT_ID = "" # Fill with your agent id
            client = dataiku.api_client()
            project = client.get_default_project()
            llm = project.get_llm(AGENT_ID)
            completion = llm.new_completion()
            resp = completion.with_message("How to run an agent?").execute()
            if resp.success:
                print(resp.text)

    .. group-tab:: DKUChatModel

        With the :class:`DKUChatModel<dataikuapi.dss.langchain.DKUChatModel>`, for more information,
        refer to :ref:`ce-llm-mesh-langchain-integration`:

        .. code-block:: python
            :name: ce/agents/dkuchatmodel/using-agent
            :caption: Using your agent

            AGENT_ID = "" # Fill with your agent id
            langchain_llm = project.get_llm(AGENT_ID).as_langchain_chat_model()
            resp = langchain_llm.invoke("How to run an agent?")
            print(resp.content)



Streaming (in a notebook)
-------------------------

.. tabs::
    .. group-tab:: Native DSSLLM

        .. code-block:: python
            :name: ce/agents/native-dssllm/streaming-agent
            :caption: Streaming (in a notebook)

            from dataikuapi.dss.llm import DSSLLMStreamedCompletionChunk, DSSLLMStreamedCompletionFooter
            from IPython.display import display, clear_output

            AGENT_ID = "" # Fill with your agent id
            client = dataiku.api_client()
            project = client.get_default_project()
            llm = project.get_llm(AGENT_ID)
            completion = llm.new_completion()
            completion.with_message("Who is the customer fdouetteau? Please provide additional information.")

            gen = ""
            for chunk in completion.execute_streamed():
                if isinstance(chunk, DSSLLMStreamedCompletionChunk):
                    gen += chunk.data["text"]
                    clear_output()
                    display("Received text: %s" % gen)
                elif isinstance(chunk, DSSLLMStreamedCompletionFooter):
                    print("Completion is complete: %s" % chunk.data)

    .. group-tab:: DKUChatModel

        .. code-block:: python
            :name: ce/agents/dkuchatmodel/streaming-agent
            :caption: Streaming (in a notebook)

            from IPython.display import display, clear_output

            AGENT_ID = "" # Fill with your agent id
            langchain_llm = project.get_llm(AGENT_ID).as_langchain_chat_model()
            resp = langchain_llm.stream("Who is the customer fdouetteau? Please provide additional information.")

            gen = ""
            for r in resp:
                clear_output()
                gen += r.content
                display(gen)

Asynchronous Streaming (in a notebook)
--------------------------------------

.. code-block:: python
    :name: ce/agents/async-agent-use
    :caption: Asynchronous Streaming (in a notebook)

    import asyncio
    from IPython.display import display, clear_output

    async def func(response):
        gen = ""
        async for r in response:
            clear_output()
            gen += r.content
            display(gen)

    AGENT_ID = "" # Fill with your agent id
    langchain_llm = project.get_llm(AGENT_ID).as_langchain_chat_model()
    resp = langchain_llm.astream("Who is the customer fdouetteau? Please provide additional information.")


    await(func(resp))

Code Agents
===========

In Dataiku, you can implement a custom agent in code that leverages models from the LLM Mesh,
LangChain, and its wider ecosystem.

The resulting agent becomes part of the LLM Mesh, seamlessly integrating into your AI workflows.

Dataiku includes basic code examples to help you get started.
Below are more advanced samples that showcase full-fledged examples of agents built with LangChain and LangGraph.
They both work with the internal code environment for retrieval-augmented generation to avoid any code env issue.


.. tabs::
    .. group-tab:: Support Assistant (LangChain)

        This support agent is designed to handle customer inquiries efficiently. With its tools, it can:

        - retrieve relevant information from an FAQ database
        - log issues for follow-up when immediate answers aren't available
        - escalate complex requests to a human agent when necessary.

        We have tested it on this [Paris Olympics FAQ dataset](https://www.kaggle.com/datasets/sahityasetu/paris-2024-olympics-faq),
        which we used to create a knowledge bank with the Embed recipe.
        We have embedded a column containing both the question and the corresponding answer.
        Use the agent on inquiries like: `How will transportation work in Paris during the Olympic Games?` or
        `I booked a hotel for the Olympic games in Paris, but never received any confirmation. What's happening?`
        and see how it reacts!

        .. literalinclude:: /concepts-and-examples/examples/llm/code-agents/support-assistant.py
            :language: python


    .. group-tab:: Data Analysis Assistant (LangGraph)


        This data analysis agent is designed to automate insights from data.

        Given a table (from an SQL database) and its schema (list of columns with information about what they contain), it can:

        - take a user question
        - translate it into an SQL query
        - run the query and fetch the result
        - interpret the result and convert it back into natural language.

        The code below was written for [this dataset about car sales](https://www.kaggle.com/datasets/missionjee/car-sales-report).
        We used a Prepare recipe to remove some columns and parse the date to a proper format.
        Once implemented, test your agent with questions like:
        `What were the top 5 best-selling car models in 2023?` or
        `What was the year-over-year evolution in the Scottsdale region regarding the number of sales?`.

        .. literalinclude:: /concepts-and-examples/examples/llm/code-agents/data_analysis_assistant.py
            :language: python

.. _ce/agents/creating-your-code-agent:

Creating your code agent
------------------------

All code agents must implement the ``BaseLLM`` class.
The ``BaseLLM`` class is somewhat similar to this implementation:

.. code-block:: python
    :name: ce/agents/creating-agent
    :caption: Creating your code agent

    class BaseLLM(BaseModel):
        """The base interface for a Custom LLM"""

        # Implement this for synchronous answer
        def process(self, query: SingleCompletionQuery, settings: CompletionSettings,
                    trace: SpanBuilder) -> CompletionResponse:
            raise _NotImplementedError

        # Implement this for asynchronous answer
        async def aprocess(self, query: SingleCompletionQuery, settings: CompletionSettings,
                           trace: SpanBuilder) -> CompletionResponse:
            raise _NotImplementedError

        # Implement this for a streamed answer
        def process_stream(self, query: SingleCompletionQuery, settings: CompletionSettings,
                           trace: SpanBuilder) -> Iterator[StreamCompletionResponse]:
            raise _NotImplementedError
            yield

        # Implement this for a asynchronous streamed answer
        async def aprocess_stream(self, query: SingleCompletionQuery,
                                  settings: CompletionSettings, trace: SpanBuilder) -> \
                AsyncIterator[StreamCompletionResponse]:
            raise _NotImplementedError
            yield

Generating an answer from a code agent follows the same rules, whether the agent is synchronous, streamed, or not.

1. Get an LLM (refer to :ref:`ce_llm_agent_using_your_agent`, for more details).
2. Process the input (and the settings).
3. Potentially manipulate the trace.
4. Invoke the LLM (refer to :ref:`ce_llm_agent_using_your_agent`, for more details).
5. Return the answer (refer to :ref:`ce_llm_agent_using_your_agent`, for more details).

1. Process the input without history
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to deal with the last message, you should only take the last  ``content`` from the query,
as highlighted in the following code:

.. tabs::
    .. group-tab:: Native DSSLLM

        .. code-block:: python
            :name: ce/agents/native-dssllm/without-history
            :caption: Process the input without history
            :emphasize-lines: 1

                prompt = query["messages"][-1]["content"]
                completion = llm.new_completion().with_message(prompt)

                ## .../...

                llm_resp = completion.execute()


    .. group-tab:: DKUChatModel
        .. code-block:: python
            :name: ce/agents/dkuchatmodel/without-history
            :caption: Process the input without history
            :emphasize-lines: 1

            prompt = query["messages"][-1]["content"]
            message = [HumanMessage(prompt)]

            ## .../...

            llm_resp = llm.invoke(message)


2. Process the input with history
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your intent is to use your agent conversationally,
you may need to process the query to provide the whole context to the LLM.

.. tabs::
    .. group-tab:: Native DSSLLM
        .. code-block:: python
            :name: ce/agents/native-dssllm/with-history
            :caption: Process the input with history

            completion = llm.new_completion()
            for m in query.get('messages'):
                completion.with_message(m.get('content'), m.get('role'))

            ## .../...

            llm_resp = completion.execute()

    .. group-tab:: DKUChatModel
        .. code-block:: python
            :name: ce/agents/dkuchatmodel/with-history
            :caption: Process the input with history

            messages = []
            for m in query.get('messages'):
                match m.get('role'):
                    case 'user':
                        messages.append(HumanMessage(m.get('content')))
                    case 'assistant':
                        messages.append(AIMessage(m.get('content')))
                    case 'system':
                        messages.append(SystemMessage(m.get('content')))
                    case 'tool':
                        messages.append(ToolMessage(m.get('content')))
                    case _:
                        logger.info('Unknown role', m.get('content'))

            ##.../...

            llm.invoke(messages)


3. Adding trace information
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: python
    :name: ce/agents/adding-trace
    :caption: Adding trace information

    with trace.subspan("Invoke the LLM") as subspan:
        ai_msg = llm.invoke(messages)
        subspan.attributes['messages']= str(messages)

Handling the trace
==================

Once you have a trace, you can access the ``inputs``, ``outputs``, and ``attributes`` objects,
or if you prefer, you can use the :meth:`~dataikuapi.dss.llm_tracing.SpanBuilder.to_dict` method.
Then you can modify these objects to reflect your needs.
You can add a child to the trace (use the :meth:`~dataikuapi.dss.llm_tracing.SpanBuilder.subspan` method)
or append another trace to the current trace (use the :meth:`~dataikuapi.dss.llm_tracing.SpanBuilder.append_trace` method).

In the following code example, we consider ``trace`` to be a trace,
and ``dict`` to be a dictionary built using ``trace.to_dict()``.

.. code-block:: python
    :caption: Adding input information on a trace

    trace.inputs["additional_information"] = "Useful information"
    dict["inputs"].update({"additional_information" : "Useful information"})

.. code-block:: python
    :caption: Adding output information on a trace

    trace.outputs["additional_information"] = "Useful information"
    dict["outputs"].update({"additional_information" : "Useful information"})

.. code-block:: python
    :caption: Adding attributes information on a trace

    trace.attributes["additional_information"] = "Useful information"
    dict["attributes"].update({"additional_information" : "Useful information"})

.. code-block:: python
    :caption: Changing the name of a trace

    dict["name"] = "New name"

.. note::
    Updating the name is rarely helpful, as you can provide the name with the :meth:`~dataikuapi.dss.llm_tracing.SpanBuilder.subspan` method


Agent Tools
===========

Listing your agent tools
------------------------

The following code lists all the Agent Tools with their names and IDs, which you can reuse in the code samples listed later on this page.

.. code-block:: python
    :name: ce/agents/agent-tools/listing
    :caption: Listing your agent tools

    tools_list = project.list_agent_tools()

    for tool in tools_list:
        print(f"{tool.name} - {tool.id}")

Creating your agent tool
------------------------

.. code-block:: python
    :name: ce/agents/agent-tools/creating
    :caption: Creating your agent tool

    import dataiku

    KB_ID = "" # fill with the ID of your Knowledge Bank

    client = dataiku.api_client()
    project = client.get_default_project()
    vector_search_tool_creator = project.new_agent_tool("VectorStoreSearch")
    vector_search_tool = vector_search_tool_creator.with_knowledge_bank(KB_ID).create()

Modifying your agent tool settings
----------------------------------

.. code-block:: python
    :name: ce/agents/agent-tools/modifying
    :caption: Modifying your agent tool settings

    settings = vector_search_tool.get_settings()
    print(settings.params['maxDocuments'])
    settings.params['maxDocuments'] = 8
    settings.save()

Running your agent tool
-----------------------

.. code-block:: python
    :name: ce/agents/agent-tools/running
    :caption: Running your agent tool

    vector_search_tool.run({"searchQuery": "best review"})

Deleting your agent tool
------------------------

.. code-block:: python
    :name: ce/agents/agent-tools/deleting
    :caption: Deleting your agent tool

    vector_search_tool.delete()

Retrieval-augmented LLM agent
=============================

Creating your RAG agent
-----------------------

.. code-block:: python
    :name: ce/agents/rag-agent/listing
    :caption: Creating your RAG agent

    import dataiku

    KB_ID = "" # fill with your Knowledge Bank's id
    LLM_ID = "" # fill with your LLM id

    client = dataiku.api_client()
    project = client.get_default_project()
    rag_agent = project.create_retrieval_augmented_llm("MyRAG", KB_ID, LLM_ID)

Modifying your RAG agent settings
---------------------------------

.. code-block:: python
    :name: ce/agents/rag-agent/modifying
    :caption: Modifying your RAG agent settings

    LLM_ID2 = "" # fill with an alternate LLM id
    rag_agent_settings = rag_agent.get_settings()
    active_version = rag_agent_settings.active_version
    v_rag_agent_settings = rag_agent_settings.get_version_settings(active_version)
    v_rag_agent_settings.llm_id = LLM_ID2
    rag_agent_settings.save()

Running your RAG agent
----------------------

.. code-block:: python
    :name: ce/agents/rag-agent/running
    :caption: Running your RAG agent

    response = rag_agent.as_llm().new_completion().with_message("What will inflation in Europe look like and why?").execute()
    print(response.text)

Deleting your RAG agent
-----------------------

.. code-block:: python
    :name: ce/agents/rag-agent/deleting
    :caption: Deleting your RAG agent

    rag_agent.delete()

Visual Agent
============

Creating your visual agent
--------------------------

.. code-block:: python
    :name: ce/agents/visual-agent/creating
    :caption: Creating your visual agent

    import dataiku

    TOOL_ID = "" # fill with your agent tool's id

    client = dataiku.api_client()
    project = client.get_default_project()
    agent = project.create_agent("visual1", "TOOLS_USING_AGENT")


Modifying your visual agent settings
------------------------------------

.. code-block:: python
    :name: ce/agents/visual-agent/modifying
    :caption: Modifying your visual agent settings

    TOOL_ID = "" # fill with your agent tool id
    tool = project.get_agent_tool(TOOL_ID)
    agent_settings = agent.get_settings()
    versionned_agent_settings = agent_settings.get_version_settings("v1")
    versionned_agent_settings.llm_id = LLM_ID
    versionned_agent_settings.add_tool(tool)
    agent_settings.save()

Running your visual agent
-------------------------

.. code-block:: python
    :name: ce/agents/visual-agent/running
    :caption: Running your visual agent

    response = agent.as_llm().new_completion().with_message("tell me everything you know about Dataiku").execute()
    response.text

Deleting your visual agent
--------------------------

.. code-block:: python
    :name: ce/agents/visual-agent/deleting
    :caption: Deleting your visual agent

    agent.delete()

Extracting sources
==================
Suppose you have an agent that is querying a knowledge bank. You can retrieve the sources
by using the following code snippet:

.. code-block:: python
    :name: ce/agents/extracting-sources
    :caption: Extracting sources

    #AGENT_ID = "" # Fill with your agent id
    langchain_llm = project.get_llm(AGENT_ID).as_langchain_chat_model()
    messages = "What is the climate in 2024"
    current_agent_response = langchain_llm.invoke(messages)
    last_trace = current_agent_response.response_metadata.get('lastTrace', None)
    attributes = last_trace.get('attributes')
    completionResponse = attributes.get('completionResponse')
    additionalInformation = completionResponse.get('additionalInformation')
    sources = additionalInformation.get('sources')
    for source in sources:
        items = source.get('items')
        for document in items:
            print(document)

Running multiple asynchronous agents
=====================================

Sometimes, achieving a task requires running multiple agents.
Some of the tasks handled by the agent can be run in parallel.

.. tabs::

    .. group-tab:: Using ``asyncio``

        To run agents in parallel, you need to invoke agents asynchronously, and be sure that your agent/tool is ``async`` compatible.
        The :meth:`~langchain.chains.llm.LLMChain.ainvoke` method allows the user to make an asynchronous call.

        .. code-block:: python
            :name: ce/agents/asyncio/running-async-agents
            :caption: Running multiple asynchronous agents

            import asyncio

            AGENT_ID = "" ## Fill you your agent ID (agent:xxxxxxxx)
            langchain_llm = project.get_llm(AGENT_ID).as_langchain_chat_model()

            async def queryA():
                try:
                    print("Calling query A")
                    resp = langchain_llm.ainvoke("Give all the professional information you can about the customer with ID: fdouetteau. Also include information about the company if you can.")
                    response = await resp
                    return response
                except:
                    return None

            async def queryB():
                try:
                    print("Calling query B")
                    resp = langchain_llm.ainvoke("Give all the professional information you can about the customer with ID: tcook. Also include information about the company if you can.")
                    response = await resp
                    return response
                except:
                    return None

            ## Uncomment this if you are running into a notebook
            # import nest_asyncio
            # nest_asyncio.apply()

            loop = asyncio.get_event_loop()
            results = [asyncio.create_task(query) for query in [queryA(), queryB()]]
            loop.run_until_complete(asyncio.wait(results))
            for r in results:
                if r.result() and r.result().content:
                    print(r.result().content)

    .. group-tab:: Using Langchain Runnable

        .. code-block:: python
            :name: ce/agents/langchain-runnable/running-async-agents
            :caption: Running multiple asynchronous agents

            from langchain_core.runnables import RunnableParallel
            from langchain_core.output_parsers import StrOutputParser
            from langchain_core.prompts import PromptTemplate

            AGENT_ID = "" ## Fill you your agent ID (agent:xxxxxxxx)
            ids = ["id1", "id2"] ## Use your data
            langchain_llm = project.get_llm(AGENT_ID).as_langchain_chat_model()
            local_prompt = PromptTemplate(
                input_variables=["user_id"],
                template="Give all the professional information you can about the customer with ID: {user_id}. Also include information about the company if you can."
            )
            runnable_map = {
                f"chain_{i}": local_prompt.partial(user_id=ida) | langchain_llm
                for i,ida in enumerate(ids)}
            parallel_chain = RunnableParallel(runnable_map)
            results = parallel_chain.invoke({})
            for key, output in results.items():
                print(f"{key}: {getattr(output, 'content', output)}")

Reference documentation
=======================

Classes
-------
.. autosummary::
    dataikuapi.DSSClient
    dataikuapi.dss.langchain.DKUChatModel
    dataikuapi.dss.llm.DSSLLM
    dataikuapi.dss.llm.DSSLLMCompletionQuery
    dataikuapi.dss.project.DSSProject


Functions
---------
.. autosummary::
    ~dataikuapi.dss.llm_tracing.SpanBuilder.append_trace
    ~dataikuapi.dss.llm.DSSLLMCompletionsQuery.execute
    ~dataikuapi.dss.llm.DSSLLMCompletionQuery.execute_streamed
    ~dataikuapi.DSSClient.get_default_project
    ~dataikuapi.dss.project.DSSProject.get_llm
    ~dataikuapi.dss.project.DSSProject.list_llms
    ~dataikuapi.dss.llm.DSSLLM.new_completion
    ~dataikuapi.dss.llm_tracing.SpanBuilder.subspan
    ~dataikuapi.dss.llm_tracing.SpanBuilder.to_dict
    ~dataikuapi.dss.llm.DSSLLMCompletionQuery.with_message
