from .baseloader import load_docs

LANGCHAIN_SITEMAP = "https://docs.langchain.com/sitemap.xml"

def load_langchain_docs():

    docs = load_docs(LANGCHAIN_SITEMAP, "langchain")

    print("Loaded Langchain Docs!")

    return docs

