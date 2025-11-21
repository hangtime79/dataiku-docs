import dataiku
from dataiku.langchain.dku_llm import DKUChatModel
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

LLM_ID = "<fill with your LLM Id>"
KB_ID = "fill with your Knowledge Bank Id"

# Retrieve the vectore store through the Knowledge Bank
client = dataiku.api_client()
project = client.get_default_project()
kb = dataiku.KnowledgeBank(id=KB_ID, project_key=project.project_key)
vector_store = kb.as_langchain_vectorstore()

# Create the LLM access
dkullm = DKUChatModel(llm_id=LLM_ID, temperature=0)
system_prompt = """Always state when an answer is unknown. Do not guess or fabricate a response.
    {context}"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)
# Create the chain that will combine documents in the context with the prompt
question_answer_chain = create_stuff_documents_chain(dkullm, prompt)

# an example user query
user_query = "What will inflation in Europe look like and why?"

# First, perform a similarity search with the vector store
search_results = vector_store.similarity_search(user_query, k=10)

# Run the enriched query
resp = question_answer_chain.invoke({"context": search_results, "input": user_query})
print(resp)
