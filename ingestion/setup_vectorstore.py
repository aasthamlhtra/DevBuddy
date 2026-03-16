from .build_vectorstore import store_documents
from .chunker import chunk_documents
from .loaders import fastapi_loader, flask_loader, langchain_loader

fastapi_docs = fastapi_loader.load_fastapi_docs()
# flask_docs = flask_loader.load_flask_docs()
# langchain_docs = langchain_loader.load_langchain_docs()

chunked_fastapi_docs = chunk_documents(fastapi_docs)
# chunked_flask_docs = chunk_documents(flask_docs)
# chunked_langchain_docs = chunk_documents(langchain_docs)

store_documents(chunked_fastapi_docs, "fastapi_docs")
# store_documents(chunked_flask_docs, "flask_docs")
# store_documents(chunked_langchain_docs, "langchain_docs")