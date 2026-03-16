from .baseloader import load_docs

FLASK_SITEMAP = "https://flask.palletsprojects.com/sitemap.xml"

def load_flask_docs():

    docs = load_docs(FLASK_SITEMAP, "flask")

    print("Loaded Flask Docs!")

    return docs

