from langchain_community.document_loaders.sitemap import SitemapLoader


def load_docs(sitemap_url : str, framework : str):

    sitemap_loader = SitemapLoader(
        web_path = sitemap_url
    )

    docs = sitemap_loader.load()

    for doc in docs:
        doc.metadata["framework"] = framework

    return docs
