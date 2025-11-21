Query an LLM/Agent
##################

This tool calls an LLM or Agent in the LLM Mesh. You configure a system prompt and target LLM.

When calling the tool, it gets a prompt as input, and it queries the target LLM with the system prompt + input, and responds with the LLM response.

This can be surprising at first sight: after all, tools are usually called from agents, that are already LLMs. Why call another LLM?

There are several possible use cases for this "agent-inception":

* Separation of concerns: An Agent can use this to call another Agent, without having to know all the details. This other Agent can be developed by another team, use another technology, ...

* Keeping the Agent on track: if you have complex tasks to accomplish, having a single agent with many different tools can lead to worse responses. Cutting it into several smaller agents that are orchestrated by an "overarching Agent" that uses Query an LLM/Agent tools can help improve the answers.

* Performance and Cost Management: Some LLMs are very good at some specific tasks (such as OpenAI o3 for advanced reasoning), but slow and expensive, and it would not be reasonable to use them as the "main" LLM of the Agent. Using a Query an LLM/Agent tool leveraging them allows you to use these specific LLMs only for a subset of tasks: while the task is not too complex, the main LLM handles it, but it can delegate more advanced tasks to the advanced reasoning LLM.
