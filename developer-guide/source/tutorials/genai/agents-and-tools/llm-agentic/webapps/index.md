# Building a Web Application with the agent

In the previous parts of this series ([here](../tools/index) and
[here](../agents/index)), you saw how to define tools and create an LLM-based
agent capable of answering queries by calling those tools. This part
demonstrates how to build an interactive web interface so end-users can
interact with this functionality in a browser. Different frameworks can be used,
as detailed below.

## Creating a webapp

First, you'll set up the webapp framework, alongside creating the necessary
infrastructure within Dataiku. Choose your preferred framework and follow
the necessary steps.

::::{tabs}
:::{group-tab} Dash

Dash applications can be created as Code webapps with the following steps:

- Create a new webapp by clicking on **</> > Webapps**
- Click the **+New webapp**, choose the **Code webapp**, then click on the
  **Dash** button, choose the **An empty Dash app** option, and choose a
  meaningful name
- In the **Code env** option of the **Settings** tabs, select the Python
code environment with the packages defined in the
{ref}`prerequisites <llm-agentic-prereqs>` for this tutorial series
- You'll need to add the following packages specific to Dash to the code env

  ```python  
    dash # tested with 2.18.2
    dash-bootstrap-components # tested with 1.6.0
  ```

:::

:::{group-tab} Gradio

 Gradio applications run in Code Studios in Dataiku. To create a new application,
 follow the steps outlined in {doc}`/tutorials/webapps/gradio/first-webapp/index`.
 In short, the steps are:

- Create a Code Studio template that includes a code env with the required
packages defined in the {ref}`prerequisites <llm-agentic-prereqs>` for this tutorial series
- You'll need to add the following packages specific to Gradio to the code env

  ```python  
  gradio # tested with 3.48.0
  ```

- Create a Code Studio based on the template
- Add the full script provided at the end of this tutorial 
to the Code Studio in the `gradio/app.py` file
- *If you have access to the Code Studio's workspace via a VSCode 
or Jupyter Lab block, then you can see the full path of the file at
`/home/dataiku/workspace/code_studio-versioned/gradio/app.py`*

:::

:::{group-tab} Voila

 Voila applications run in Code Studios in Dataiku. To create a new application,
 follow the steps outlined in {doc}`/tutorials/webapps/voila/first-webapp/index`. In short, the steps are:

- Create a Code Studio template with JupyterLab Server and Voilà blocks.
- When adding the Voilà block, include the required packages (`duckduckgo_search==7.1.1`) defined
in the {ref}`prerequisites <llm-agentic-prereqs>` in the `Additional Python modules` option.
- Create a Code Studio based on the template.
- Using the JupyterLab interface, add the full script provided
at the end of this tutorial to the Code Studio
in the `code_studio-versioned/visio/app.ipynb` file.

:::
::::

```{note}
The predefined tools need to be present in a location accessible via code.
You can place the file (available [here](../common-assets/tools.json) for download) 
in `</> > Libraries`. You can find detailed instructions in the 
{ref}`previous tutorial<llm-agentic-predefined-tools>`, plus why it is useful to follow this approach.

For similar reasons of modularity, helper functions common among the application scripts are also placed in a separate file. Specifically, the functions `create_chat_session`, `get_customer_details`, `search_company_info` and `process_tool_calls` are included in the `utils.py` (also available for [download](../common-assets/utils.py)). It needs to be placed in the same location as `tools.json`, following the same steps.
```

## Passing on the task to the agent

After choosing our webapp framework, the crucial step is implementing the LLM agent functionality.
It follows a consistent pattern across frameworks. Regardless of which one, the chat session is
defined the same way.

Similar to the agent in [Part 2](../agents/index), the chat session is created by calling the
`create_chat_session()` function. It sets up an LLM via the LLM Mesh with the system prompt.

The application sends the information obtained about the customer to the agent. You'll see how each
framework collects this information below. A loop is created to process the tool calls and responses,
until no more tool calls are needed. The agent then returns the final response.

## Calling the agent

The next step is connecting the user interface to the agent's functionality.
Here's how each framework runs the agent.

::::{tabs}
:::{group-tab} Dash

Dash wires everything up with callbacks to process user queries. Connect the
button to a callback function that invokes the agent with the `@app.callback`
decorator. The `update_output()` function allows the user to enter the customer ID
and click the button to trigger the function with the agent. The agent then
processes the input via a chat session and returns the final response.

```{literalinclude} assets/app-dash.py
:language: python
:caption: Calling the agent
:lines: 39-54
```

:::

:::{group-tab} Gradio

Gradio's chat interface also uses a similar function that processes the current message and
all previous conversation turns. The `chat_with_agent()` function that calls the agent
has two parameters:

- message: current user message
- history: list of (user, assistant) message tuples

The user inputs and conversation history are forwarded to the `chat_with_agent()` function.
The agent then processes the input via a chat session and returns the final response.

```{literalinclude} assets/app-gradio.py
:language: python
:caption: Calling the agent
:lines: 14-23
```

:::

:::{group-tab} Voila

In Voila, you'll define a function `process_agent_response()` to deliver queries to the LLM
via a chat session. It has two parameters: `chat`, which is the chat session, and `query`,
which is the user's message. The agent processes the user's query via the chat session.

```{literalinclude} assets/app-voila.py
:language: python
:caption: Calling the agent
:lines: 13-15
```

:::
::::

## Creating the layout

Finally, to provide a UI for this agent functionality, you'll build an interface with components
that allows users to interact with it. Each framework offers its own approach.

The layout gathers user inputs (e.g. message with customer ID) and passes it to the agent functions
for each framework. The agent then returns the result to be displayed in the UI.

::::{tabs}
:::{group-tab} Dash

Create a Dash layout that constructs an application like
{ref}`Figure 1<tutorials_genai_llm_agentic_webapps_image_dash>`,
consisting of an input Textbox for entering a customer ID and an output Textarea.

The callback function described above takes the user's requests from the input Textbox and passes the
entered customer ID to `create_chat_session()`, rendering the final agent response in the output Textarea.

```{literalinclude} assets/app-dash.py
:language: python
:caption: Dash layout
:lines: 17-37
```

```{eval-rst}
.. _tutorials_genai_llm_agentic_webapps_image_dash:

.. figure:: ./assets/webapp-llmmesh-agent-dash-result.png
    :align: center
    :class: with-shadow image-popup w400
    :alt: Figure 1: LLM Agentic -- webapp.
    
    Figure 1: LLM Agentic -- webapp.
```

:::

:::{group-tab} Gradio

Unlike Dash's component-based approach, Gradio offers a more conversation-focused interface.
Using its `ChatInterface` class, create a layout like
{ref}`Figure 1<tutorials_genai_llm_agentic_webapps_image_gradio>` that includes:

- A chat message input field for queries
- The conversation history including the agent's replies
- Optional features like example prompts

```{literalinclude} assets/app-gradio.py
:language: python
:caption: Gradio layout
:lines: 51-60
```

```{eval-rst}
.. _tutorials_genai_llm_agentic_webapps_image_gradio:

.. figure:: ./assets/webapp-llmmesh-agent-gradio-result.png
    :align: center
    :class: with-shadow image-popup
    :alt: Figure 1: LLM Agentic -- webapp.
    
    Figure 1: LLM Agentic -- webapp.
```

:::

:::{group-tab} Voila

Voila uses JupyterLab's `ipywidgets` (imported here as `widgets`) to provide the UI for
user interactions. The `query_input` provides a textbox to collect the user query and a
`button` to trigger `on_button_click()`. That function calls `process_agent_response()`
with the query and displays the returned message in the `result` widget.

```{literalinclude} assets/app-voila.py
:language: python
:caption: Voila layout
:lines: 36-66
```

```{eval-rst}
.. _tutorials_genai_llm_agentic_webapps_image_voila:

.. figure:: ./assets/webapp-llmmesh-agent-voila-result.png
    :align: center
    :class: with-shadow image-popup
    :alt: Figure 1: LLM Agentic -- webapp.
    
    Figure 1: LLM Agentic -- webapp.
```

:::
::::

## Conclusion

You now have an application that:

1. Uses an LLM-based agent to process queries
2. Imports predefined tools to complement LLM capabilities
3. Provides a user-friendly web interface

You could enhance this interface by adding a history of previous searches or
creating a more detailed and cleaner results display. This example
provides a foundation for building more complex LLM-based browser applications,
leveraging tool calls and webapp interfaces.

::::{tabs}
:::{group-tab} Dash

````{dropdown} [Dash application code](assets/app-dash.py)
```{literalinclude} assets/app-dash.py
:language: python
:caption: Longer code block with full script
:name: tutorials-genai-webapp-dash-llmmesh
```
````

:::

:::{group-tab} Gradio

````{dropdown} [Gradio application code](assets/app-gradio.py)
```{literalinclude} assets/app-gradio.py
:language: python
:caption: Longer code block with full script
:name: tutorials-genai-webapp-gradio-llmmesh
```
````

:::

:::{group-tab} Voila

````{dropdown} [Voila application notebook](assets/app.ipynb)
```{literalinclude} assets/app-voila.py
:language: python
:caption: Longer code block with full script
:name: tutorials-genai-webapp-voila-llmmesh
```
````

:::
::::
