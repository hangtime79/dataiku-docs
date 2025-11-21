import dataiku
from langchain.chains.question_answering import load_qa_chain
from dataiku.langchain.dku_llm import DKUChatModel

KB_ID = "" # Fill with your KB id
GPT_LLM_ID = ""  # Fill with your LLM-Mesh id

# Retrieve the knowledge base and LLM handles
client = dataiku.api_client()
project = client.get_default_project()
kb = dataiku.KnowledgeBank(id=KB_ID, project_key=project.project_key)
vector_store = kb.as_langchain_vectorstore()
gpt_lc = DKUChatModel(llm_id=GPT_LLM_ID, temperature=0)

# Create the question answering chain
chain = load_qa_chain(gpt_lc, chain_type="stuff")
query = "What will inflation in Europe look like and why?"
search_results = vector_store.similarity_search(query)

# ⚡ Get the results ⚡
resp = chain({"input_documents":search_results, "question": query})
print(resp["output_text"])

# Inflation in Europe is expected to remain high in the near term due to
# persistently high inflation that will prevent a rapid easing of monetary
# policy in most economies and weigh on private consumption. Projected fiscal
# consolidation further dampens the outlook. Risks such as an escalation of
# the conflict in the Middle East could increase energy prices, tighten
# financial conditions, and negatively affect confidence.

# Geopolitical risks in the region, including an escalation of the Russian
# Federation’s invasion of Ukraine, are elevated and could materialize.
# Higher-than-anticipated inflation or a weaker-than-expected recovery in
# the euro area would also negatively affect regional activity. However, by
# 2024-25, global inflation is expected to decline further, underpinned by
# the projected weakness in global demand growth and slightly lower
# commodity prices.