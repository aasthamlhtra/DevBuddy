from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from app.rag.pipeline.retriever import get_retriever

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(collection_name: str):
    retriever = get_retriever(collection_name)
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_template("""
        You are DevBuddy, a precise AI assistant for developers.

        Use ONLY the documentation excerpts below.
        If the answer is not found, say you don't know.

        Documentation:
        ----------------
        {context}
        ----------------

        Question:
        {question}

        Answer:
        """)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain