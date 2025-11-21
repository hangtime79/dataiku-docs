Building and using an agent with Dataiku's LLM Mesh and Langchain
*****************************************************************

Large Language Models' (LLMs) impressive text generation capabilities can be further enhanced by integrating them
with additional modules: planning, memory, and tools.
These LLM-based agents can perform tasks such as accessing databases,
incorporating contextual understanding from external sensors,
or interfacing with other software to execute more complex actions.
This integration allows for more dynamic and practical applications,
making LLMs active participants in decision-making processes.

This tutorial will construct an LLM agent using a practical use case.
The use case involves retrieving customer information based on a provided ID and
fetching additional data about the customer's company utilizing an internet search.
By the end of this tutorial,
you will have a structured understanding of integrating Language Models with external tools to create functional and efficient agents.

Prerequisites
#############

* Dataiku >= 12.6.2
* Python >= 3.9
* A code environment with the following packages:

  .. code-block:: python

    langchain # tested with 0.3.25
    duckduckgo_search #tested with 8.0.2

* An SQL dataset called ``pro_customers_sql`` in the flow, like the one shown in :ref:`Table 1<tutorial-genai-agent-table1>`.

.. _tutorial-genai-agent-table1:
.. csv-table:: Table 1: ``pro_customers_sql``
   :file: ./assets/pro_customers.csv
   :header-rows: 1

LLM initialization and library import
#####################################

To begin with, you need to set up a development environment
by importing some necessary libraries and initializing the chat LLM you want to use to create the agent.
The tutorial relies on the LLM Mesh for this and the Langchain package to orchestrate the process.
The ``DKUChatModel`` class allows you to call a model previously registered in the LLM Mesh
and make it recognizable as a Langchain chat model for further use.

.. code-block:: python
    :caption: Code 1: LLM Initialization

    import dataiku

    # Prepare the LLM
    from dataiku.langchain.dku_llm import DKUChatModel

    LLM_ID = "" # Replace with a valid LLM id

    llm = DKUChatModel(llm_id=LLM_ID, temperature=0)


.. tip::

    You'll need to provide DKUChatModel with an ``llm_id``, a Dataiku internal ID used in the LLM Mesh.
    The :ref:`documentation<ce/llm-mesh/get-llm-id>` provides instructions on obtaining an ``LLM ID``.
    The following code snippet will print you an exhaustive list of all the models to which your project has access.

    .. code-block:: python

        import dataiku
        client = dataiku.api_client()
        project = client.get_default_project()
        llm_list = project.list_llms()
        for llm in llm_list:
            print(f"- {llm.description} (id: {llm.id})")


Tools' definition
#################

In this section, you will define the external tools that your LLM agent will use to perform more advanced tasks.
In our case, these tools include:

* **Dataset lookup tool**: used to execute SQL queries on the ``pro_customers_sql`` dataset
  to retrieve customer information (name, role, company), given a customer ID.
  :ref:`Code 2<tutorial_genai_agent_code2>` shows an implementation of this tool.
* **Internet search tool**: used to perform internet searches to fetch more detailed information about the customer’s company.
  :ref:`Code 3<tutorial_genai_agent_code3>` shows an implementation of this tool.


.. note::

    Langchain offers three main ways to define custom tools: the ``@tool`` decorator,
    the ``StructuredTool.from_function()`` method that takes a Python function as input,
    or the class method, which extends the built-in ``BaseTool`` class and provides metadata as well as a ``_run`` method (at least).

    The tutorial defines the tool here using the last option because we noticed that the LLM tends to use them more consistently.
    But don't hesitate to try all three methods yourself.


.. code-block:: python
    :caption: Code 2: Definition of the Dataset lookup tool
    :name: tutorial_genai_agent_code2

    from langchain.tools import BaseTool
    from dataiku import SQLExecutor2
    from langchain.pydantic_v1 import BaseModel, Field
    from typing import Type
    from dataiku.sql import Constant, toSQL, Dialects


    class CustomerInfo(BaseModel):
        """Parameter for GetCustomerInfo"""
        id: str = Field(description="customer ID")


    class GetCustomerInfo(BaseTool):
        """Gathering customer information"""

        name: str = "GetCustomerInfo"
        description: str = "Provide a name, job title and company of a customer, given the customer's ID"
        args_schema: Type[BaseModel] = CustomerInfo

        def _run(self, id: str):
            dataset = dataiku.Dataset("pro_customers_sql")
            table_name = dataset.get_location_info().get('info', {}).get('quotedResolvedTableName')
            executor = SQLExecutor2(dataset=dataset)
            cid = Constant(str(id))
            escaped_cid = toSQL(cid, dialect=Dialects.POSTGRES) # Replace by your DB
            query_reader = executor.query_to_iter(
                 f"""SELECT * FROM {table_name}  where "id"={escaped_cid}""")
            for (user_id, name, job, company) in query_reader.iter_tuples():
                return f"The customer's name is \"{name}\", holding the position \"{job}\" at the company named \"{company}\""
            return f"No information can be found about the customer {id}"

        def _arun(self, name: str):
            raise NotImplementedError("This tool does not support async")

.. note::
    The SQL query might be written differently depending on your SQL Engine.


.. code-block:: python
    :caption: Code 3: Definition of the Internet search tool
    :name: tutorial_genai_agent_code3

    from duckduckgo_search import DDGS

    class CompanyInfo(BaseModel):
        """Parameter for the GetCompanyInfo"""
        name: str = Field(description="Company's name")


    class GetCompanyInfo(BaseTool):
        """Class for gathering in the company information"""

        name: str = "GetCompanyInfo"
        description: str = "Provide general information about a company, given the company's name."
        args_schema: Type[BaseModel] = CompanyInfo

        def _run(self, name: str):
            results = DDGS().text(name + " (company)", max_results=1)
            result = "Information found about " + name + ": " + results[0]["body"] + "\n" \
                if len(results) > 0 and "body" in results[0] \
                else None
            if not result:
                results = DDGS().text(name, max_results=1)
                result = "Information found about " + name + ": " + results[0]["body"] + "\n" \
                    if len(results) > 0 and "body" in results[0] \
                    else "No information can be found about the company " + name
            return result

        def _arun(self, name: str):
            raise NotImplementedError("This tool does not support async")


LLM agent creation
##################


With the tools defined, the next step is to create an agent that can effectively utilize these tools.
This tutorial uses the `ReAct <https://react-lm.github.io/>`__ logic,
which combines the LLM's ability for reasoning (e.g., chain-of-thought prompting, etc.)
and acting (e.g., interfacing with external software, etc.) through a purposely crafted prompt.

Alternatively, it is possible to use the tool calling logic, when the LLM supports tool calls.
More information can be found in the :ref:`tool calls section <llm-mesh-tool-calls>` of the
developer guide.


.. tabs::
    .. group-tab:: ReAct

        .. note::
            Langchain offers a hub for community members to share pre-built prompt templates and
            other resources. The prompt below has been taken from there, and it is also
            possible to `fetch it directly <https://smith.langchain.com/hub/hwchase17/react>`__
            with the following code:

            .. code-block:: python

                # Only need if you want to use a default prompt (may require langchainhub dependency)
                from langchain import hub
                prompt = hub.pull("hwchase17/react")

        .. code-block:: python
            :caption: Code 4: LLM agent creation

            # Initializes the agent
            from langchain_core.prompts import ChatPromptTemplate
            from langchain.agents import AgentExecutor, create_react_agent
            from langchain.tools import StructuredTool

            # Link the tools
            tools = [GetCustomerInfo(), GetCompanyInfo()]
            tool_names = [tool.name for tool in tools]

            prompt = ChatPromptTemplate.from_template(
            """Answer the following questions as best you can. You have only access to the following tools:

            {tools}

            Use the following format:

            Question: the input question you must answer
            Thought: you should always think about what to do
            Action: the action to take, should be one of {tool_names}
            Action Input: the input to the action
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question

            Begin!

            Question: {input}
            Thought:{agent_scratchpad}""")

            agent = create_react_agent(llm, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools,
               verbose=True, return_intermediate_steps=True, handle_parsing_errors=True)


    .. group-tab:: Tool calls

        .. note::
            Langchain offers a hub for community members to share pre-built prompt templates and
            other resources. The prompt below has been taken from there, and it is also
            possible to `fetch it directly <https://smith.langchain.com/hub/hwchase17/openai-tools-agent>`__
            with the following code:

            .. code-block:: python

                # Only need if you want to use a default prompt (may require langchainhub dependency)
                from langchain import hub
                prompt = hub.pull("hwchase17/openai-tools-agent")

        .. code-block:: python
            :caption: Code 4: LLM agent creation

            # Initializes the agent
            from langchain_core.prompts import ChatPromptTemplate
            from langchain.agents import AgentExecutor, create_tool_calling_agent

            # Link the tools
            tools = [GetCustomerInfo(), GetCompanyInfo()]

            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant"),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ])

            agent = create_tool_calling_agent(llm, tools, prompt)
            agent_executor = AgentExecutor(
                agent=agent, tools=tools,
                verbose=True, return_intermediate_steps=True, handle_parsing_errors=True
            )


        .. note::

            The Langchain tool calling ``AgentExecutor`` attempts to query the LLM with a
            streaming strategy. When the LLM supports tool calls but does not support response
            streaming, it is still possible to use the tool calling agent by setting the parameter
            ``stream_runnable=False`` in the call to the ``AgentExecutor`` constructor.

.. tip::

    The ``AgentExecutor`` class has a ``callback``
    `parameter <https://api.python.langchain.com/en/latest/agents/langchain.agents.agent.AgentExecutor.html#langchain.agents.agent.AgentExecutor.callbacks>`__
    that can be used with packages like ``mlflow`` for debugging and tracing purposes.
    For inspiration, refer to our `LLM StarterKit project <https://gallery.dataiku.com/projects/EX_LLM_STARTER_KIT/flow/?zoneId=Gzn9KXV>`__ on the Dataiku Gallery.


LLM agent invocation
####################

Finally, you can run the ``agent_executor``.
Depending on the level of detail you want to see about the intermediate steps
and the "decisions" taken by the agents, Langchain offers several methods and a debug mode.
We are showing them below.


.. tabs::
    .. group-tab:: ReAct

        .. code-block:: python
            :caption: Code 5: Simple invocation

            from langchain.globals import set_debug

            set_debug(False) ## Set to True to get debug traces
            customer_id = "fdouetteau"

            ## This will directly return the output from the defined input
            agent_executor.invoke(
                {
                    "input": f"""Give all the professional information you can about the customer with ID: {customer_id}. Also include information about the company if you can.""",
                    "tools": tools,
                    "tool_names": tool_names
                })["output"]


        .. code-block:: python
            :caption: Code 6: Iteration on intermediate steps

            ## You can also iterate on intermediate steps, to print them or run any tests, with the .iter() method
            i=1
            for step in agent_executor.iter({
                    "input": f"""Give all the professional information you can about the customer with ID: {customer_id}.
                    Also include information about the company if you can.""",
                    "tools": tools,
                    "tool_names": tool_names
                }):
                print("\n", "*"*20, f"Step: {i}")
                if output := step.get("intermediate_step"):
                    action, value = output[0]
                    print(output[0])
                    print("-"*80)
                    print(action.log)
                    print("+"*80)
                    print(value)
                    i += 1
                elif output := step.get('output'):
                        print(output)


    .. group-tab:: Tool calls

        .. code-block:: python
            :caption: Code 5: Simple invocation

            from langchain.globals import set_debug

            set_debug(False) ## Set to True to get debug traces
            customer_id = "fdouetteau"

            ## This will directly return the output from the defined input
            agent_executor.invoke({
                "input": f"Give all the professional information you can about the customer with ID: {customer_id}. Also include information about the company if you can.",
            })["output"]


        .. code-block:: python
            :caption: Code 6: Iteration on intermediate steps

            ## You can also iterate on intermediate steps, to print them or run any tests, with the .iter() method
            i=1
            for step in agent_executor.iter({
                "input": f"Give all the professional information you can about the customer with ID: {customer_id}. Also include information about the company if you can.",
            }):
                print("\n", "*"*20, f"Step: {i}")
                if output := step.get("intermediate_step"):
                    action, value = output[0]
                    print(output[0])
                    print("-"*80)
                    print(action.log)
                    print("+"*80)
                    print(value)
                    i += 1
                elif output := step.get('output'):
                        print(output)

Wrapping up
###########

This tutorial provided a walk-through for building an LLM-based agent capable of interacting with external tools to fetch and process information.
Modularizing the approach - from initialization and tool definition to the creation and invocation of the agent -
ensures clarity, reusability, and efficiency, suitable for tackling similar tasks.