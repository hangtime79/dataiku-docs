import dataiku
from dataiku.llm.python import BaseLLM
from dataiku.langchain import LangchainToDKUTracer
from langchain.tools import Tool
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

## 1. Set Up Vector Search for FAQs
# Here, we are using a knowledge bank from the flow, build with our native Embed recipe.
# We make it a Langchain retriever and pass it to our first tool.

KB_ID = "" # fill with the ID of your Knowledge Bank
LLM_ID = "" # fill with your LLM id

faq_retriever = dataiku.KnowledgeBank(id=KB_ID).as_langchain_retriever()
faq_retriever_tool = Tool(
    name="FAQRetriever",
    func=faq_retriever.get_relevant_documents,
    description="Retrieves answers from the FAQ database based on user questions."
)


## 2. Define (fake) Ticketing & Escalation Tools
# Simulated ticket creation function

def create_ticket(issue: str):
    # Here, you would typically use the API to your internal ticketing tool.
    return f"Ticket created: {issue}"


ticketing_tool = Tool(
    name="CreateTicket",
    func=create_ticket,
    description="Creates a support ticket when the issue cannot be resolved automatically."
)


# Simulated escalation function
def escalate_to_human(issue: str):
    # This function could send a notification to the support engineers, for instance.
    # It can be useful to attach info about the customer's request, sentiment, and history.
    return f"Escalation triggered: {issue} has been sent to a human agent."


escalation_tool = Tool(
    name="EscalateToHuman",
    func=escalate_to_human,
    description="Escalates the issue to a human when it's too complex, or the user is upset."
)

## 3. Build the LangChain Agent
# Define LLM for agent reasoning
llm = dataiku.api_client().get_default_project().get_llm(LLM_ID).as_langchain_chat_model()

# Agent tools (FAQ retrieval + ticketing + escalation)
tools = [faq_retriever_tool, ticketing_tool, escalation_tool]
tool_names = [tool.name for tool in tools]

# Define the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         """You are an AI customer support agent. Your job is to assist users by:
         - Answering questions using the FAQ retriever tool.
         - Creating support tickets for unresolved issues.
         - Escalating issues to a human when necessary."""),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# Initialize an agent with tools.
# Here, we define it as an agent that uses OpenAI tools.
# More options are available at https://python.langchain.com/api_reference/langchain/agents.html

agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

agent_executor.invoke({"input": "How will transportation work in Paris during the Olympic Games?"})

class MyLLM(BaseLLM):
    def __init__(self):
        pass

    def process(self, query, settings, trace):
        prompt = query["messages"][0]["content"]
        tracer = LangchainToDKUTracer(dku_trace=trace)
        # Wrap the agent in an executor
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        response = agent_executor.invoke({"input": prompt}, config={"callbacks": [tracer]})
        return {"text": response["output"]}
