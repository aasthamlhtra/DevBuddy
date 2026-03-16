from .baseloader import load_docs

FASTAPI_SITEMAP = "https://fastapi.tiangolo.com/sitemap.xml"

def load_fastapi_docs():

    docs = load_docs(FASTAPI_SITEMAP, "fastapi")

    print("Loaded FastAPI docs!")

    return docs
