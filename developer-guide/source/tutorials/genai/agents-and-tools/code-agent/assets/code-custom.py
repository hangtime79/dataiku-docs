from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
import dataiku
from dataiku.llm.python import BaseLLM

project = dataiku.api_client().get_default_project()

OPENAI_CONNECTION_NAME = "REPLACE_WITH_YOUR_CONNECTION_NAME"  # example: "openAI"


def find_tool(name: str):
    for tool in project.list_agent_tools():
        if tool["name"] == name:
            return project.get_agent_tool(tool['id'])
    return None


# If you know the tool IDs, you can use them directly.
get_customer = find_tool("Get Customer Info").as_langchain_structured_tool()
get_company = find_tool("Get Company Info").as_langchain_structured_tool()

tools = [get_customer, get_company]


class MyLLM(BaseLLM):
    def __init__(self):
        pass

    def process(self, query, settings, trace):
        project = dataiku.api_client().get_default_project()
        llm = project.get_llm(f"openai:{OPENAI_CONNECTION_NAME}:gpt-5-mini").as_langchain_chat_model(completion_settings=settings)
        llm_with_tools = llm.bind_tools(tools)

        messages = [m for m in query["messages"] if m.get("content")]
        iterations = 0
        while True:
            iterations += 1
            if iterations < 10:
                with trace.subspan("Invoke LLM with tools") as llm_invoke_span:
                    llm_response = llm_with_tools.invoke(messages)
            else:
                with trace.subspan("Invoke LLM without tools") as llm_invoke_span:
                    llm_response = llm.invoke(messages)

            if len(llm_response.tool_calls) == 0:
                return {"text": llm_response.content}

            with llm_invoke_span.subspan("Call the tools") as tools_subspan:
                messages.append(llm_response)
                for tool_call in llm_response.tool_calls:
                    with tools_subspan.subspan("Call a tool") as tool_subspan:
                        tool_subspan.attributes["tool_name"] = tool_call["name"]
                        tool_subspan.attributes["tool_args"] = tool_call["args"]
                        if tool_call["name"] == get_customer.name:
                            tool_output = get_customer(tool_call["args"])
                        elif tool_call["name"] == get_company.name:
                            tool_output = get_company(tool_call["args"])
                        else:
                            raise ValueError("unknown tool: " + tool_call["name"])
                    messages.append(ToolMessage(tool_call_id=tool_call["id"], content=tool_output))
