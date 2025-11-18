# General Imports
from langchain_community.document_loaders import GithubFileLoader

# Package Imports
from app.core import app_config

def get_document_loader(repo_name: str, repo_branch: str)-> GithubFileLoader:
    """Returns a GithubFileLoader object for a given repository and branch."""
    return GithubFileLoader(
        repo = repo_name,
        branch = repo_branch,
        access_token = app_config.github_personal_access_token,
        github_api_url = "https://api.github.com",
        file_filter=lambda file_path: file_path.endswith(
            (".py",".yml",".yaml","Dockerfile","md")
         )
    )