# Agents and Tools for Generative AI

Large Language Models (LLMs) are powerful but have inherent limitations in areas like real-time data access,
mathematical computations, and specialized domain knowledge.
To overcome these constraints,
you can use certain tools and techniques to extend LLM capabilities through external functions,
structured workflows, and integrations with other systems.

This section explores key approaches for enhancing LLM performance,
from basic tool integration to complex agentic behaviors,
enabling more accessible and even more powerful AI applications.

```{admonition} Concepts & examples

You can find code samples on this subject in the Developer Guide: {doc}`/concepts-and-examples/agents`.

``` 

## Agents

### Visual agent and custom tool

[This tutorial](/tutorials/plugins/custom-tools/generality/index) shows how to build a custom tool.
Once you have built a custom tool, or if you want to use tools provided by Dataiku,
you can follow [this tutorial](./visual-agent/index).

### Code Agent
[This tutorial](./code-agent/index) introduces how you can use {doc}`refdoc:agents/code-agents` in Dataiku.
If you want to create your agent, you should follow [this tutorial](/tutorials/plugins/agent/generality/index).
You can also create an [Inline Python Tool](inline-python-tool/index) in a simplified experience with inline code.
As described in the [multi-agent tutorial](./multi-agent/index), you will need a multi-agent system when working on complex tasks.
You may also need to define your [LLM Connection](/tutorials/plugins/llm-connection/generality/index).

### LLM Mesh agentic applications

[This tutorial](./llm-agentic/index) series demonstrates how to build agentic applications using the LLM Mesh in Dataiku.

### Model Context Protocl (MCP)

[This tutorial](./mcp/index) series demonstrates how to build custom & 3rd party MCP Servers using Code studios and Webapps in Dataiku.

### Langchain agents

In addition, you could also build agents in Dataiku using the Langchain framework.
Langchain enhances LLM capabilities by integrating planning, memory, and tools modules.
This allows LLMs to perform more complex tasks like accessing databases or interfacing with other software.

You can find the tutorial [here](./agent/index).

## Processing
### Using JSON outputs
[This tutorial](./json-output/index) demonstrates how to process and get structured outputs via the LLM Mesh.

## Prompt
### Auto Prompt Strategies with DSPy

[This tutorial](./auto-prompt/index) demonstrates the usage of an auto-prompting library and its usage.

## Monitoring
### Adding traces to your agent

[This tutorial](./traces/index) demonstrates the usage of traces to help you understand your agent's behavior.


```{toctree}
:maxdepth: 1
:hidden:

./inline-python-tool/index
/tutorials/plugins/custom-tools/generality/index
./visual-agent/index
./code-agent/index
/tutorials/plugins/agent/generality/index
/tutorials/plugins/llm-connection/generality/index
./multi-agent/index
./llm-agentic/index
./mcp/index
./agent/index
./json-output/index
./auto-prompt/index
./traces/index
```
