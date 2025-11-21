import dataiku
import os
import json
from gpt_utils.wb_reporter import build_qa_chain
from gpt_utils.wb_reporter import run_qa_chain
from gpt_utils.wb_reporter import RegionOutlookList
from gpt_utils.wb_reporter import TOPICS
from gpt_utils.models import get_gpt_llm
from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate


# Set up LLM
chat = get_gpt_llm(secret_name="OPENAI_API_KEY")

# Load the vector database
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


# --- Chain #1: retrieve the list of regions

# Retrieve formatting instructions from output parser
reg_parser = CommaSeparatedListOutputParser()
reg_pfi = reg_parser.get_format_instructions()

# Define prompt template
reg_prompt = PromptTemplate(template="{context}\n{question}\n{fmt}",
                               input_variables=["context", "question"],
                               partial_variables={"fmt": reg_pfi})

# Define and run question-answering chain
reg_query = "List the main regions studied inside a comma-separated string."
reg_chain = load_qa_chain(chat, chain_type="stuff", prompt=reg_prompt)
reg_simsearch = vector_db.similarity_search(reg_query, include_metadata=True)
regions = run_qa_chain(chain=reg_chain,
                       query=reg_query,
                       vec_db=vector_db)

# --- Chain #2: write summary for each region

# Retrieve formatting instructions from output parser
rpt_parser = PydanticOutputParser(pydantic_object=RegionOutlookList)
rpt_chain = build_qa_chain(llm=chat, parser=rpt_parser)

topics_str = ",".join(TOPICS.keys())
q = f"""
For each region in {regions} describe in a few sentences the state of the 
following topics: {topics_str}.
"""

reports = run_qa_chain(chain=rpt_chain,
                       query=q,
                       vec_db=vector_db)

# Write final results in output dataset
output_dataset = dataiku.Dataset("wb_regional_reports")
output_schema = [
    {"name": "region_name", "type": "string"}
]
for k in TOPICS.keys():
    output_schema.append({"name": k, "type": "string"})
output_dataset.write_schema(output_schema)
with output_dataset.get_writer() as w:
    for item in json.loads(reports).get("items"):
        w.write_row_dict(item)

