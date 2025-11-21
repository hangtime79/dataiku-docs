Using tools
#############


There are two main ways that tools in Dataiku are used:

Visual Agent
==============

:doc:`/agents/visual-agents` directly leverage tools for their working. This is a fully no-code usage of tools

API
====

Tools come with a complete API that allow you to integrate tools usage in your own code. This can be in a :doc:`Code Agent </agents/code-agents>` or any other kind of code.

Native API
----------

Dataiku tools can be used directly. Here is an example of calling an instance of the Dataset Lookup tool

.. code-block:: python

    import dataiku
    tool = dataiku.api_client().get_default_project().get_agent_tool("my-tool-1")

    output = tool.run({
        "filter" : {
            "operator": "EQUALS",
            "column": "company_name",
            "value": "Dataiku"
        }
    })

    # Matched rows are in
    output["output"]["rows"]


LangChain API
--------------

Dataiku tools can be converted into LangChain Structured Tools to be used in any LangChain / LangGraph compatible code:

.. code-block:: python

    import dataiku
    tool = dataiku.api_client().get_default_project().get_agent_tool("my-tool-1")
    
    lctool = tool.as_langchain_structured_tool()
    
    output = lctool.invoke({
        "filter" : {
            "operator": "EQUALS",
            "column": "company_name",
            "value": "Dataiku"
        }        
    })
    
    output["rows"]

Importantly, this "lctool" is a fully structured LangChain Tool, including knowing its schema. It can therefore immediately be used with a LangChain tool-aware LLM

.. code-block:: python

    llm_with_tools = llm.bind_tools([lctool])

    # Assuming that the dataset contains revenues of companies
    llm_with_tools.invoke(("user", "What is the revenue of Apple"))


Tool descriptor
---------------

A key component of tools is that they are self-describing. You can obtain a "tool descriptor" that lists:

* Name
* Description (that can be passed to a LLM)
* Input schema (as a JSON schema)

For example, a :doc:`Dataset lookup tool <dataset-lookup>` has a descriptor like this (when working on the "titanic" dataset):

.. code-block:: python

    import dataiku
    tool = dataiku.api_client().get_default_project().get_agent_tool("titanic1")
    descriptor = tool.get_descriptor()

    {
      "name": "titanic1_KttcvQ",
      "description": "Get records (up to 10) from dataset kaggle_titanic_train\n\nThe columns that are available for you to lookup are:\n\n  * PassengerId (type: STRING)\n  * Name (type: STRING)\n  * Age (type: STRING)\n",
      "inputSchema": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://dataiku.com/agents/tools/datasets/row-lookup/input",
        "title": "Lookup settings for a row of a dataset",
        "type": "object",
        "properties": {
          "filter": {
            "type": "object",
            "description": "The filter to search for the records",
            "properties": {
              "operator": {
                "type": "string",
                "description": "Filter operator. One of EQUALS, NOT_EQUALS, GREATER_THAN, LESS_THAN, DEFINED, NOT_DEFINED, CONTAINS, MATCHES (regex), AND, OR"
              },
              "column": {
                "type": "string",
                "description": "On which column it applies. Not applicable to AND and OR"
              },
              "value": {
                "type": "string",
                "description": "Value to compare. Not applicable to AND, OR, DEFINED, NOT_DEFINED. Can be a string or a number. Beware, don't put between quotes if you mean a number."
              },
              "clauses": {
                "type": "array",
                "description": "Boolean clauses. Only applies to AND and OR. These sub-clauses are of the same type as the current element",
                "items": {
                  "$ref": "#/properties/filter"
                }
              }
            }
          }
        }
      }
    }

Context
--------

In addition to the "input" and "output" of the tool, a tool takes an input a "context".

The context is an arbitrary JSON dictionary, that can be used to pass any kind of information you would like. The LLM of the agent is not aware of the context.

A typical usage example is as follows: you are building a customer support agent. This agent has a tool looking up information about a customer. At some point in the conversation with the customer, the agent needs to lookup information about the customer. However, you don't want the information about "who is the customer" to be part of the tool input, because there is a risk that it could be manipulated by the customer. Therefore, the customer information is passed by your code to the tool, and the tool uses the context rather than what's in the input to filter on the customer.

When using a Visual Agent, the Visual Agent passes the context that it receives to all tools that it calls.

