import dataiku
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain


# Creating your Knowledge Bank
KB_NAME = ""
EMBED_LLM_ID = ""

client = dataiku.api_client()
project = client.get_default_project()
dss_kb = project.create_knowledge_bank(KB_NAME, "CHROMA", EMBED_LLM_ID)

# Adding embeded content to your Knowledge Bank
FILE_URL = "https://bit.ly/GEP-Jan-2024" # Update as needed

loader = PyPDFLoader(FILE_URL)
documents = []
async for page in loader.alazy_load():
    documents.append(page)

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE,
                                 separator='\n',
                                 chunk_overlap=CHUNK_OVERLAP,
                                 length_function=len)
chunked_documents = splitter.split_documents(documents)

kb_core = dss_kb.as_core_knowledge_bank()

with kb_core.get_writer() as writer:
    langchain_vs = writer.as_langchain_vectorstore()
    langchain_vs.add_documents(chunked_documents)

# Query a LLM with improved context from your Knowledge Bank
LLM_ID = ""  # Fill with your LLM-Mesh id

vector_store = kb_core.as_langchain_vectorstore()
llm = project.get_llm(llm_id=LLM_ID).as_langchain_chat_model()

# Create the question answering chain
chain = load_qa_chain(llm, chain_type="stuff")
query = "What will inflation in Europe look like and why?"
search_results = vector_store.similarity_search(query)

# ⚡ Get the results ⚡
resp = chain({"input_documents":search_results, "question": query})
print(resp["output_text"])