# Defining and using tools with the LLM Mesh

## Introduction

Large Language Models (LLMs) are incredibly versatile in understanding and
generating human-like text. Yet they still have notable limitations. When LLMs
struggle with operations requiring precise mathematical calculations or updated
data, external tools can complement them. Tools are predefined functions that an
LLM can call during a conversation to solve specific problems, like performing
calculations or querying databases.

In this first part of a [series of tutorials](../index), you'll learn how to
integrate tools into your workflows using the LLM Mesh, a centralized and
governed interface for accessing models from multiple providers. You'll define
tools, implement tool calls, and see how the LLM interacts with these tools.

## Defining Tools

First, let's define a tool in the context of an LLM. Tools are functions invoked
during a conversation to perform a predefined task. Like functions, they accept
specific parameters and return a response via a process outside the LLM
workflow, which is then used as part of the conversation.

Tools can be defined using a JSON schema, specifying parameters and their types.
This schema helps the LLM understand what kind of input the tool requires and
what output it can expect. JSON schemas are also helpful by providing
clear, human-readable descriptions and metadata.

In this tutorial, you will define two tools:

1. Customer Information Tool - retrieves customer details from a database
2. Company Information Tool - searches the internet for company information

```{literalinclude} assets/chat.py
:language: python
:lines: 14-49
:caption: JSON schema for tool definition
```

## Adding the tool with an LLM Mesh workflow

You'll create a client to interact with a specific LLM Mesh connection. Next,
you'll start a new chat, which is basically a completion task for the model
based on user and tool inputs. To that chat, you'll add tools for retrieving
customer data and fetching company information.

As with any LLM workflow, providing context to the model is essential. This
context defines the model's role as well as what it can expect from the user,
the tool and how to interpret the inputs it receives. You'll specify that the
LLM acts as a helpful assistant with access to customer and company information.

```{literalinclude} assets/chat.py
:language: python
:lines: 12, 51-75
:caption: Chat settings and context
```

## Chatting with the LLM to use the tool

Once the model shows it understands these questions, you can ask it to retrieve
customer information. At this point, the LLM decides whether it needs to call
the tool to help with the user's request. Once it does, the model calls the tool
as a response. The parameters needed to retrieve the information are extracted
from the conversation, i.e., from the user's statement.

```{literalinclude} assets/chat.py
:language: python
:lines: 77-89
:caption: Chatting with the LLM to extract parameters
```

Then, you'll need to use the extracted request to call the tool function. Let's
implement a simple Python function (`process_tool_calls`) that calls other
functions that retrieve customer information (`get_customer_info`) or search
for the company online (`search_company_info`) based on the tool that was called
and using the parameters provided. The `tool_call_result` is added back to the
conversation.

```{attention}
The SQL query might be written differently depending on your SQL Engine.
```

```{literalinclude} assets/chat.py
:language: python
:lines: 92-118
:caption: Functions to retrieve customer information & search for company info
```

Each time the tool is called, the tool call, and the function output are logged
in the conversation history. This helps the LLM record what was executed and
integrate the tool workflow into the conversation.

```{literalinclude} assets/chat.py
:language: python
:lines: 138-142
:caption: Recording tool call and output
```

## Checking the results

To verify whether and how the LLM used the tools, you can look at the
history of the chat. To access the entire history, you can use
`chat.cq["messages"]`.

Let's take a closer look at a possible outcome to see how tool calls are
structured.

```{literalinclude} assets/chat.py
:language: python
:lines: 144-191
:caption: Printing out the chat history
```

## Wrapping Up

This tutorial, teaches you how to use tool calls via the LLM Mesh.
By defining and implementing tools,
the LLM seamlessly integrates additional functionality like querying databases or performing computations.
The LLM Mesh also manages context and message history.

When building robust, extensible workflows, this approach might come in handy.
Plus, with the LLM Mesh, you can worry less about manual message tracking or 
complex integrations, especially when handling multiple models.

The [next tutorial](../agents/index) in this series covers how to create an LLM-based agent that
uses the multiple tools defined in this tutorial.

````{dropdown} [chat.py](assets/chat.py)
```{literalinclude} assets/chat.py
:language: python
:caption: Longer code block with full script
:name: tutorials-genai-tools-llmmesh
```
````
