from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
db = Chroma(
    collection_name="fastapi_docs",
    persist_directory="C:/Users/aasth/Desktop/DevBuddy/vectorstore/chroma_db",
    embedding_function=OpenAIEmbeddings()
)
print(db._collection.count()) 