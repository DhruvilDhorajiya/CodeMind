from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from app.repositories.github_loader import (
    InvalidGitHubRepositoryError,
    RepositoryCloneError,
)
from app.repositories.service import import_github_repository

app = FastAPI(
    title="CodeMind",
    description="RAG assistant for understanding codebases",
)

class AddRepositoryRequest(BaseModel):
    repository_url: HttpUrl


@app.post("/repositories")
def add_repository(request: AddRepositoryRequest):
    try:
        result = import_github_repository(
            str(request.repository_url)
        )
    except InvalidGitHubRepositoryError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except RepositoryCloneError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return {
        "repository_id": result["repository_id"],
        "owner": result["owner"],
        "name": result["name"],
        "commit_sha": result["commit_sha"],
    }

