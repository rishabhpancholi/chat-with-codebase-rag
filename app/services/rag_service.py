# General Imports
from langchain_core.retrievers import BaseRetriever

# Package Imports
from app.rag import get_document_loader,TextPreprocessor,VectorStoreBuilder


def rag_pipeline(repo_name: str, repo_branch: str)-> BaseRetriever:
    """Function for running the RAG pipeline"""
    document_loader = get_document_loader(repo_name,repo_branch)
    documents = document_loader.load()

    text_preprocessor = TextPreprocessor(documents)
    documents = text_preprocessor.preprocess()

    vector_store_builder = VectorStoreBuilder(documents,repo_name,repo_branch)
    vector_store = vector_store_builder.build_vector_store()

    retriever = vector_store.as_retriever()

    return retriever

if __name__ == "__main__":
    rag_pipeline("rishabhpancholi/fake-job-detection-mlops-project","main")

