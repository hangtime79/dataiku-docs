import dataiku
import os
import tiktoken

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

FILE_URL = "https://bit.ly/GEP-Jan-2024" # Update as needed

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

enc = tiktoken.encoding_for_model("gpt-4")
splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE,
                                 separator='\n',
                                 chunk_overlap=CHUNK_OVERLAP,
                                 length_function=len)

docs_dataset = dataiku.Dataset("document_splits")
docs_dataset.write_schema([
    {"name": "split_id", "type": "int"},
    {"name": "text", "type": "string"},
    {"name": "page", "type": "int"},
    {"name": "nb_tokens", "type": "int"}
])


# Read PDF file, split it into smaller chunks and write each chunk data + metadata
# in the output dataset
splits = PyPDFLoader(FILE_URL) \
    .load_and_split(text_splitter=splitter)

with docs_dataset.get_writer() as w:
    for i, s in enumerate(splits):
        d = s.dict()
        w.write_row_dict({"split_id": i,
            "text": d["page_content"],
            "page": d["metadata"]["page"],
            "nb_tokens": len(enc.encode(d["page_content"]))
            })
