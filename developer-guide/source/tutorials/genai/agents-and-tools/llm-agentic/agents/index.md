# Creating an LLM-based agent that uses multiple tools

## Introduction

The [previous part](../tools/index) of this tutorial series showed how to define
external tools so an LLM can retrieve data or perform specialized tasks. Now,
let’s see how to integrate these tools into an agent capable of handling
multi-step queries in a flexible conversation.

In this tutorial, you’ll create an agent to deploy multiple tools to
manage user queries in a conversational workflow. Whenever a user asks for
information, the agent decides how to respond.
It could answer directly, but more
often it might have to engage a “tool.” In this example, the agent relies on two
tools from the previous tutorial. To recap, one retrieves a user's name,
position, and company based on an ID, while a second tool searches the Internet
to find company information.

````{dropdown} [tools.json](../common-assets/tools.json)
```{literalinclude} ../common-assets/tools.json
:language: JSON
:caption: Previously defined tools
```
````

## Agentic workflow

The workflow of our LLM-based agent is broken down into several steps:

1. The agent receives a user query and analyzes its contents.
2. It checks available tools that might help answer the query.
3. When a tool is needed, the agent calls the corresponding function, waits for
   the output, and integrates it into its reasoning.
4. Finally, it produces a coherent response that it returns to the user.

The corresponding and processing functions remain the same as in the previous
part and are now part of a chat session involving the agent. Namely,
`get_customer_details(customer_id)`, `search_company_info(company_name)`,
and `process_tool_calls(tool_calls)` are called within the agent’s conversation
flow.

(llm-agentic-predefined-tools)=
## Using pre-defined tools

Since the tools are well-defined, they are included as a JSON file:
[tools.json](../common-assets/tools.json). Place the file in a location
accessible to code in Dataiku. An option is to use `</> > Libraries`. If you
upload the file in a folder named `python`, you can access it in any Python code
in the project.

Separating tools into a JSON file improves modularity and maintenance,
allowing easy updates without altering the core of the application's code.
It also keeps tool definitions separate from the main application's logic,
making the code easier to understand and manage.

!["Put your file within </> >
Libraries"](assets/codelibs-tools-json.png){.image-popup}

## Creating the agent

The agent is built around a function `create_chat_session` which sets up the LLM
with the system prompt and tool definitions. You need to provide context to the
LLM using a prompt that explains its role and how to use the tools. The code
snippet below shows the essential pieces of the agent: system prompt definition,
tool import, and conversation flow management. A function `create_chat_session`
focuses on this setup, making sure the LLM is ready to use the appropriate
tools.

```{literalinclude} assets/conversation.py
:language: python
:lines: 37-59
:emphasize-lines: 7
:caption: Defining a chat session
```

## Accessing tools

During the next step, `process_query()` guides the conversation with the user.
By structuring requests in a loop, the agent can make multiple calls to tools if
the user’s question is complex. For example, if the question involves a
customer’s detailed profile along with their company information, the agent can
call one function for the customer’s data and another function for the company’s
data before returning a final result.

```{literalinclude} assets/conversation.py
:language: python
:lines: 61-87
:caption: How a single query is resolved
```

## Wrapping up

Here's what a conversation with the agent could look like:

```{literalinclude} assets/conversation.py
:language: python
:lines: 89-109
:caption: Example usage
```

- Now, you have an LLM-based agent that can handle multi-tool calling.  
- The system prompt and tool definitions provide a flexible and iterable way of
  guiding the LLM.  
- The chat session could be designed to make as many tool calls as needed to
  retrieve the required information or limit tool usage, according to the user’s
  needs.

In the [next part](../webapps/index), you’ll learn how to surface this agent in
a browser-based web application.

```{attention}
The SQL query might be written differently depending on your SQL Engine.
```


````{dropdown} [conversation.py](assets/conversation.py)
```{literalinclude} assets/conversation.py
:language: python
:caption: Longer code block with full script
:name: tutorials-genai-agent-llmmesh
```
````
