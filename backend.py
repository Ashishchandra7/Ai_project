from fastapi import FastAPI
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline

app = FastAPI()

# Free embedding model
embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Load vector database
db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)

# Free local LLM
generator = pipeline("text-generation", model="gpt2")

@app.get("/chat")
def chat(query: str):

    results = db.similarity_search(query)
    context = results[0].page_content

    prompt = f"""
    Answer using this context:
    {context}

    Question: {query}
    """

    response = generator(prompt, max_length=200)[0]["generated_text"]

    return {"answer": response}
