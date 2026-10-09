from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from app.rag.pipeline.retriever import get_retriever
from langchain_groq import ChatGroq


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_mapping_chain(frameworks: list[str]):
    retrievers = {
        fw: get_retriever(f"{fw}_docs")
        for fw in frameworks
    }

    llm = ChatGroq(model_name="llama-3.1-8b-instant")

    prompt = ChatPromptTemplate.from_template("""
        You are DevBuddy, an expert developer assistant.

        Explain the conceptual mapping between the frameworks below.

        {contexts}

        Question:
        {question}

        Provide a structured comparison with examples.
    """)

    parallel_dict = {
        fw: retrievers[fw] | RunnableLambda(format_docs)
        for fw in frameworks
    }

    chain = (
        RunnableParallel({
            "contexts": RunnableParallel(parallel_dict),
            "question": RunnablePassthrough(),
        })
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain