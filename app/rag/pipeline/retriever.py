from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

persist_directory = os.getenv("CHROMA_DB_PATH")


def get_retriever(collectionname:str):
    embeddings = OpenAIEmbeddings()

    vector_store = Chroma(
        collection_name = collectionname,
        persist_directory = persist_directory,
        embedding_function = embeddings
    )
    
    base_retriever = vector_store.as_retriever(search_kwargs = {"k" : 4})

    # multiqueryretriever = MultiQueryRetriever(
    #     base_retriever = base_retriever,
    #     llm = ChatOpenAI(),
    #     include_original = True
    # )
    return base_retriever