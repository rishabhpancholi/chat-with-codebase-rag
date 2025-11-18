# General Imports
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters.character import RecursiveCharacterTextSplitter,Language

# Package Imports
from app.models import embeddings_model

class VectorStoreBuilder:
    """Class for building a vector store from a list of documents"""
    def __init__(self, documents: list[Document], repo_name: str, repo_branch: str) -> None:
        """Initializes the VectorStoreBuilder class"""
        self.python_text_splitter = RecursiveCharacterTextSplitter.from_language(
            language = Language.PYTHON,
            chunk_size = 1000,
            chunk_overlap = 200
        )
        self.markdown_text_splitter = RecursiveCharacterTextSplitter.from_language(
            language = Language.MARKDOWN,
            chunk_size = 1000,
            chunk_overlap = 200
        )
        self.documents = documents
        self.repo_name = repo_name
        self.repo_branch = repo_branch
        self.url = "http://localhost:6333/"
        self.embedding = embeddings_model

    def build_vector_store(self)-> QdrantVectorStore:
        """Builds a Qdrant vector store from a list of documents"""
        python_chunks = self.python_text_splitter.split_documents([doc for doc in self.documents if doc.metadata["file_type"] == "py"])
        markdown_chunks = self.markdown_text_splitter.split_documents([doc for doc in self.documents if doc.metadata["file_type"]!="py"])
        total_chunks = python_chunks + markdown_chunks

        vectorstore = QdrantVectorStore.from_documents(
            documents = total_chunks,
            embedding = self.embedding,
            url = self.url,
            collection_name=f"{self.repo_name}-{self.repo_branch}".replace("/","-").replace(".","-"),
        )
        
        return vectorstore