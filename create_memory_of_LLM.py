# install library in virtual environment management
# python -m pip install pipenv
# python -m pipenv --version
# python -m pip install --user pipenv

# pipenv install langchain langchain_community langchain_huggingface faiss-cpu
# # >> pipenv install langchain{it is main branch,for take modules or library from there} langchain_community langchain_huggingface{it allow vector embedding for chumks} faiss-cpu{use for vector stores}

#  pip install pypdf
# pipenv install pypdf
# pip install pypdf
# pip install sentence-transformers
# pipenv run python .\create_memory_of_LLM.py


# Document load raw pdf files.
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Phase 1–Setup Memory for LLM (Vector Database)
# Step 1: Load raw PDF(s) >> Extract document information.
DATA_PATH="data/"
def load_pdf_files(data):
    loader = DirectoryLoader(data,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)
    
    documents=loader.load()
    return documents

documents=load_pdf_files(data=DATA_PATH)
print("Length of PDF pages: ", len(documents))


# Step 2: Create Chunks
def create_chunks(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,
                                                 chunk_overlap=50)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks

text_chunks=create_chunks(extracted_data=documents)
print("Length of Text Chunks: ", len(text_chunks))

# Step 3: Create Vector Embeddings 

def get_embedding_model():
    embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedding_model

embedding_model=get_embedding_model()

# Step 4: Store embeddings in FAISS
DB_FAISS_PATH="vectorstore/db_faiss"
db=FAISS.from_documents(text_chunks, embedding_model)
db.save_local(DB_FAISS_PATH)

