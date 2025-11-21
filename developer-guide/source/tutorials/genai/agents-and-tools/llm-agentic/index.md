# LLM Mesh agentic applications

This tutorial series demonstrates how to build agentic applications using the LLM Mesh in Dataiku. Through an example of building a customer information assistant, you'll explore three parts of an agentic workflow:

1. [Tools](./tools/index) - How to define and use tools with the LLM Mesh
2. [Agents](./agents/index) - How to create an LLM-based agent that uses multiple tools
3. [Webapps](./webapps/index) - How to build a web application with the agent

(llm-agentic-prereqs)=
## Prerequisites

- Dataiku >= 13.2
- LLM Mesh connection to a provider that supports tool calls (tested with OpenAI GPT-4; you can find a compatible list {ref}`here <llm-mesh-tool-calls>`)
- Project permissions for "Read project content" and "Write project content"
- An SQL dataset `pro_customers_sql` (a CSV file can be downloaded [here](./common-assets/pro_customers.csv) containing customer data
- Python environment with the following packages

  ```python
  duckduckgo_search # tested with 7.1.1
  ```

```{toctree}
:maxdepth: 1
:hidden:

tools/index
agents/index
webapps/index
```
