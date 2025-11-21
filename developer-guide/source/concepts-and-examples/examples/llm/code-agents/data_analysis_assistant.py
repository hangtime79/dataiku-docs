import dataiku
from dataiku.llm.python import BaseLLM
from dataiku.langchain import LangchainToDKUTracer

from langchain.prompts import ChatPromptTemplate
from dataiku import SQLExecutor2

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


LLM_ID = "" # fill with your LLM id

# Basic configuration
# Initialize LLM
llm = dataiku.api_client().get_default_project().get_llm(LLM_ID).as_langchain_chat_model()

# Connect to the sales database
dataset = dataiku.Dataset("car_data_prepared_sql")
table_name = dataset.get_location_info().get('info', {}).get('table')
table_schema = """
- `Car_id` (TEXT): Unique car ID
- `Date` (DATE): Date of the sale
- `Dealer_Name` (TEXT): Name of the car dealer
- `Company` (TEXT): Company or brand of the car
- `Model` (TEXT): Model of the car
- `Transmission` (TEXT): Type of transmission in the car
- `Color` (TEXT): Color of the car's exterior
- `Price` (INTEGER): Listed price of the car sold
- `Body_Style` (TEXT): Style or design of the car's body
- `Dealer_Region` (TEXT): Geographic region of the car dealer
"""


# Here, we are adding a dispatcher as the first step of our graph. If the user query is not related to car sales,
# the agent will simply answer that it can't talk about anything else that car sales. 
def dispatcher(state):
    """
    Decides if the query is related to car sales data or just a general question.
    
    Args:
        state (dict): The current graph state
    
    Returns:
        str: Binary decision for the next node to call
    """
    user_query = state["user_query"]

    # Classification prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a classifier that determines whether a user's query is related to car sales data.\n\n"
                "The table contains information about car sales, including:\n"
                "- Sale date & price\n"
                "- Info about the cars (brand, model, transmission, body style & color) \n"
                "- Dealer name and region\n\n"
                "If the query is related to analyzing car sales data, return 'SQL'.\n"
                "Otherwise, return 'GENERIC'."
            ),
            (
                "human", "{query}"
            )
        ]
    )

    # Get the classification result
    classification = llm.invoke(
        prompt.format_messages(query=user_query)
    ).content.strip()

    return classification


# First node, take the user input and translate it into a coherent SQL query.
def sql_translation(state):
    """
    Translates a natural language query into SQL using the database schema.
    
    Args:
        state (dict): The current graph state that contains the user_query
    
    Returns: 
        state (dict): New key added to state -- sql_query -- that contains the query to execute.
    """
    print("---Translate to SQL---")
    user_query = state["user_query"]

    # We need to pass the model our table name and schema. Adapt instructions according to your needs, of course.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an AI assistant that converts natural language questions into SQL queries.\n\n"
                "Here are the table name: {name} and schema:\n{schema}\n\n"
                "Here are some important rules:\n"
                "- Use correct table and column names\n"
                "- Do NOT use placeholders (e.g., '?', ':param').\n"
                "- The SQL should be executable in PostgreSQL, which means that table and column names should ALWAYS be double-quoted.\n"
                "- Never return your answer with SQL Markdown decorators. Just the SQL query, nothing else."
            ),
            (
                "human",
                "Convert the following natural language query into an SQL query:\n\n{query}"
            )
        ]
    )

    # Invoke LLM with formatted prompt
    sql_query = llm.invoke(
        prompt.format_messages(name=table_name, schema=table_schema, query=user_query)
    ).content
    return {"sql_query": sql_query}


# Second node, run the SQL query on the table. For this, we are using Dataiku's API.
def database_query(state):
    """
    Executes the SQL query and retrieves results.
    
    Args:
        state (dict): The current graph state that contains the query to execute.
    
    Returns: 
        state (dict): New key added to state -- query_result -- that contains the result of the query. 
                      Returns an error key if not working. 
    """
    print("---Run SQL query---")
    sql_query = state["sql_query"]

    try:
        executor = SQLExecutor2(dataset=dataset)
        df = executor.query_to_df(sql_query)
        return {"query_result": df.to_dict(orient="records")}
    except Exception as e:
        return {"error": str(e)}


# Third node, interpret the results and convert it back into natural language.
def result_interpreter(state):
    """
    Takes the raw database output and converts it into a natural language response.
    
    Args:
        state (dict): The current graph state, that contains the result of the query (or an error if it didn't work)
    
    Returns: 
        state (dict): New key added to state -- response -- that contains the final agent response. 
    """
    print("---Interpret results---")
    query_result = state.get("query_result", [])

    if not query_result:
        return {"response": "No results were found, or the query failed."}

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an AI assistant that summarizes findings from database results in a clear, human-readable format.\n"
            ),
            (
                "human", "{query_result}"
            )
        ]
    )

    formatted_prompt = prompt.format_messages(query_result=query_result)
    if len(formatted_prompt) > 1000:
        return {"response": "The returned results were too long to be analyzed. Rephrase your query."}

    summary = llm.invoke(formatted_prompt).content
    return {"response": summary}


# On the other branch of our graph, if the question is too generic, the agent will just answer with a generic response. 
def generic_response(state):
    return {
        "response": "I'm an agent specialized in car sales data analysis. I only have access to info like "
                    "sales date, price, car characteristics, and dealer name or region. "
                    "Ask me anything about car sales!"
    }


class AgentState(TypedDict):
    """State object for the agent workflow."""
    user_query: str
    sql_query: str
    query_result: list
    response: str


# Create graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("sql_translation", sql_translation)
graph.add_node("database_query", database_query)
graph.add_node("result_interpreter", result_interpreter)
graph.add_node("generic_response", generic_response)

# Define decision edges
graph.add_conditional_edges(
    START,
    dispatcher,
    {
        "SQL": "sql_translation",  # If query is about sales, go to SQL path
        "GENERIC": "generic_response"  # Otherwise, respond with a generic answer
    }
)

# Define SQL query flow
graph.add_edge("sql_translation", "database_query")
graph.add_edge("database_query", "result_interpreter")
graph.add_edge("result_interpreter", END)


class MyLLM(BaseLLM):
    def __init__(self):
        pass

    def process(self, query, settings, trace):
        prompt = query["messages"][0]["content"]
        tracer = LangchainToDKUTracer(dku_trace=trace)

        # Compile the graph
        query_analyzer = graph.compile()

        result = query_analyzer.invoke({"user_query": prompt}, config={"callbacks": [tracer]})
        resp_text = result["response"]
        sql_query = result.get("sql_query", [])

        if not sql_query:
            return {"text": resp_text}

        # If the agent did succeed, then we return the final response, as well as the sql_query, for audit purposes.
        full_resp_text = f"{resp_text}\n\nHere is the SQL query I ran:\n\n{sql_query}"
        return {"text": full_resp_text}
