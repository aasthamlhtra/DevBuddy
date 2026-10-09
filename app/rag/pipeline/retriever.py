from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

persist_directory = os.getenv("CHROMA_DB_PATH")


def get_retriever(collectionname: str):
    # Free local embedding model (runs locally without API keys)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_store = Chroma(
        collection_name=collectionname,
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    
    base_retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    return base_retriever