from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import os
from langchain_community.document_loaders import PyPDFLoader

documents = []

for file in os.listdir("data"):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(f"data/{file}")
        documents.extend(loader.load())


splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vector_db = FAISS.from_documents(docs, embedding)
vector_db.save_local("faiss_index")

print("Vector DB Created Successfully")
