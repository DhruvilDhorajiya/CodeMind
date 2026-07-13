from pathlib import Path

from app.repositories.github_loader import clone_public_repository


REPOSITORY_WORKSPACE = Path("data/repositories")


def import_github_repository(repository_url: str) -> dict:
    cloned_repository = clone_public_repository(
        repository_url=repository_url,
        workspace_root=REPOSITORY_WORKSPACE,
    )

    return {
        "repository_id": cloned_repository.repository_id,
        "owner": cloned_repository.owner,
        "name": cloned_repository.name,
        "commit_sha": cloned_repository.commit_sha,
        "local_path": str(cloned_repository.local_path),
    }