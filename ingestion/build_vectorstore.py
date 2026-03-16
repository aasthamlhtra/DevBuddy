from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()


def store_documents(documents : list[Document], collectionname : str):
    embeddings = OpenAIEmbeddings()

    vector_store = Chroma(
        collection_name = collectionname,
        embedding_function = embeddings,
        persist_directory = "C:/Users/aasth/Desktop/DevBuddy/vectorstore/chroma_db"
    )

    BATCH_SIZE = 5000   # safe under Chroma limit

    for i in range(0, len(documents), BATCH_SIZE):
        batch = documents[i:i+BATCH_SIZE]
        vector_store.add_documents(batch)
        print(f"Stored chunk {i} for {collectionname}")
        
    
    