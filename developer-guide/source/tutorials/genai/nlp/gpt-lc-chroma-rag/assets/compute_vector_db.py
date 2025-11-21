import dataiku
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

FILE_NAME = "world_bank_2023.pdf"

# Load the PDF file and split it into smaller chunks
docs_folder = dataiku.Folder("xxx") # Replace with your input folder id
pdf_path = os.path.join(docs_folder.get_path(),
                        FILE_NAME)
loader = PyPDFLoader(pdf_path)
doc = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
chunks = text_splitter.split_documents(doc)

# Retrieve embedding function from code env resources
emb_model = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(
    model_name=emb_model,
    cache_folder=os.getenv('SENTENCE_TRANSFORMERS_HOME')
)

# Index the vector database by embedding then inserting document chunks
vector_db_folder = dataiku.Folder("xxx") # Replace with your output folder id 
vector_db_path = os.path.join(vector_db_folder.get_path(),
                              "world_bank_2023_emb")
db = Chroma.from_documents(chunks,
                           embedding=embeddings,
                           metadatas=[{"source": f"{i}-wb23"} for i in range(len(chunks))],
                           persist_directory=vector_db_path)

# Save vector database as persistent files in the output folder
db.persist()
