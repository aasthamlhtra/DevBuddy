# app/rag/pipeline/router.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

from app.rag.pipeline.rag_chain import build_rag_chain
from app.rag.pipeline.mapping_chain import build_mapping_chain


def build_dynamic_single_chain(framework: str):
    collection_name = f"{framework}_docs"
    return build_rag_chain(collection_name)

SUPPORTED_FRAMEWORKS = [
    "fastapi",
    "flask",
    "langchain"
]


def build_query_classifier():
    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_template("""
You are a classifier for developer questions.

Your job:
1. Detect whether the question is about:
   - "single" framework
   - "mapping" between multiple frameworks

2. Extract the framework names mentioned.

Supported frameworks:
{frameworks}

Respond ONLY in valid JSON format:

For single framework:
{{
  "type": "single",
  "frameworks": ["framework_name"]
}}

For mapping:
{{
  "type": "mapping",
  "frameworks": ["framework1", "framework2"]
}}

Question:
{question}
""")

    parser = JsonOutputParser()

    return prompt.partial(
        frameworks=", ".join(SUPPORTED_FRAMEWORKS)
    ) | llm | parser



def build_router():

    classifier = build_query_classifier()

    def route_logic(input_dict):
        question = input_dict["question"]
        route_info = input_dict["route"]

        route_type = route_info["type"]
        frameworks = route_info["frameworks"]

        if route_type == "mapping" and len(frameworks) >= 2:
            chain = build_mapping_chain(frameworks[:2])
        else:
            framework = frameworks[0]
            chain = build_dynamic_single_chain(framework)

        return chain.invoke(question)

    router = (
        {
            "question": RunnablePassthrough(),
            "route": classifier
        }
        | RunnableLambda(route_logic)
    )

    return router