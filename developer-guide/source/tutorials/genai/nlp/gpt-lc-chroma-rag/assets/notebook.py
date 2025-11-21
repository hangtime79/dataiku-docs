###
from gpt_utils.models import get_gpt_llm

chat = get_gpt_llm(secret_name="OPENAI_API_KEY")
chat.predict("Define the role of the World Bank in one sentence.")

###

import dataiku
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma

# Load embedding function
emb_model = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=emb_model,
                                   cache_folder=os.getenv('SENTENCE_TRANSFORMERS_HOME')
)

# Load vector database
vector_db_folder_id = "xxx" # Replace with your vector db folder id
vector_db_name = "world_bank_2023_emb" 
vector_db_folder = dataiku.Folder(vector_db_folder_id)
persist_dir = os.path.join(vector_db_folder.get_path(), vector_db_name)
vector_db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

# Run similarity search query
q = "What are the 3 main perspectives regarding inflation?"
v = vector_db.similarity_search(q, include_metadata=True)

# Run the chain by passing the output of the similarity search
chain = load_qa_chain(chat, chain_type="stuff")
res = chain({"input_documents": v, "question": q})
print(res["output_text"])

###

from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate

reg_query = """
List all specific regions that were studied. Write the results in a comma-separated string.
"""

# Define the output parser
reg_parser = CommaSeparatedListOutputParser()
reg_pfi = reg_parser.get_format_instructions()

# Define the prompt template
reg_prompt = PromptTemplate(template="{context}\n{question}\n{fmt}",
                               input_variables=["context", "question"],
                               partial_variables={"fmt": reg_pfi})

# Define the question-answering chain 
reg_chain = load_qa_chain(chat, chain_type="stuff", prompt=reg_prompt)

# Run similarity search query
reg_simsearch = vector_db.similarity_search(reg_query, include_metadata=True)

# Run the chain by passing the output of the similarity chain
reg_res = reg_chain({"input_documents": reg_simsearch, "question": reg_query})
print(reg_res["output_text"])

###
