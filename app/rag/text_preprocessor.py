# General Imports
import ast
from langchain_core.documents import Document

class TextPreprocessor:
    """Class for preprocessing the loaded documents"""
    
    def __init__(self,documents):
        """Initializes the TextPreprocessor class"""
        self.documents = documents

    @staticmethod
    def python_code_parser(code: str)-> tuple[list[str],list[str]]:
        """Function for parsing python code"""
        tree = ast.parse(code)

        functions = []
        classes = []

        for node in ast.walk(tree):
           if isinstance(node, ast.FunctionDef):
               name_node = node.name
               functions.append(name_node)
           elif isinstance(node, ast.ClassDef):
               name_node = node.name
               classes.append(name_node)

        return functions,classes
    
    def metadata_tagger(self)-> list[Document]:
        """Function for tagging the file type of the document"""
        for doc in self.documents:
            if doc.metadata["path"].endswith(".yml"):
                doc.metadata["file_type"] = "yaml"
            else:
                doc.metadata["file_type"] = doc.metadata["path"].split(".")[-1]
            doc.metadata["file_name"] = doc.metadata["path"].split("/")[-1].split(".")[0]

            if doc.metadata["file_type"] == "py":
                functions,classes = self.python_code_parser(doc.page_content)
                doc.metadata["functions"] = functions
                doc.metadata["classes"] = classes
            else:
                doc.metadata["functions"] = []
                doc.metadata["classes"] = []

        return self.documents
    
    def preprocess(self)-> list[Document]:
        """Function for preprocessing the loaded documents"""
        tagged_documents = self.metadata_tagger()
        return tagged_documents

    
    
