# utils/rag_utils.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os
import shutil

# Single persistent directory — always overridden
VECTOR_STORE_PATH = "vector_store/current"

def create_rag_index(docs, pdf_name: str = "current_pdf"):
    """
    Always creates/overwrites the vector store in a fixed location.
    Old data is completely deleted and replaced.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Delete old vector store if exists
    if os.path.exists(VECTOR_STORE_PATH):
        print(f"Deleting old vector store at {VECTOR_STORE_PATH}")
        shutil.rmtree(VECTOR_STORE_PATH, ignore_errors=True)

    # Create fresh one
    os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
    
    print(f"Creating new vector store for: {pdf_name}")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_PATH
    )
    vectorstore.persist()
    print("Vector store created and saved (overwritten)")
    return vectorstore


def retrieve_context(vectorstore, query: str, k: int = 4):
    if not vectorstore:
        return ""
    try:
        docs = vectorstore.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in docs])
    except:
        return ""