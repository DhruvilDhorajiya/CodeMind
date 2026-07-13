from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl


app = FastAPI(
    title="CodeMind",
    description="RAG assistant for understanding codebases",
)

class ImportRepositoryRequest(BaseModel):
    repository_url: HttpUrl


@app.post("/repositories")
def add_repository(request: ImportRepositoryRequest):
    pass

