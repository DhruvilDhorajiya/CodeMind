import re
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from git import GitCommandError, Repo

GITHUB_HOSTS = {"github.com", "www.github.com"}

REPOSITORY_URL_PATTERN = re.compile(
    r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$"
)

@dataclass
class ClonedRepository:
    repository_id: str
    owner: str
    name: str
    local_path: Path
    commit_sha: str

class InvalidGitHubRepositoryError(ValueError):
    pass

class RepositoryCloneError(RuntimeError):
    pass


def parse_github_repository_url(repository_url: str) -> tuple[str, str]:
    parsed_url = urlparse(repository_url)

    if parsed_url.scheme != "https":
        raise InvalidGitHubRepositoryError(
            "Only HTTPS GitHub repository URLs are supported."
        )

    if parsed_url.hostname not in GITHUB_HOSTS:
        raise InvalidGitHubRepositoryError(
            "The provided URL is not a GitHub repository URL."
        )

    repository_path = parsed_url.path.strip("/")

    if repository_path.endswith(".git"):
        repository_path = repository_path[:-4]

    if not REPOSITORY_URL_PATTERN.fullmatch(repository_path):
        raise InvalidGitHubRepositoryError(
            "Expected a URL such as "
            "https://github.com/owner/repository"
        )

    owner, repository_name = repository_path.split("/", maxsplit=1)

    return owner, repository_name

def clone_public_repository(
    repository_url: str,
    workspace_root: Path,
) -> ClonedRepository:
    owner, repository_name = parse_github_repository_url(repository_url)

    repository_id = str(uuid.uuid4())
    local_path = workspace_root / repository_id

    workspace_root.mkdir(parents=True, exist_ok=True)

    try:
        repository = Repo.clone_from(
            repository_url,
            local_path,
            depth=1,
            single_branch=True,
        )
    except GitCommandError as exc:
        shutil.rmtree(local_path, ignore_errors=True)

        raise RepositoryCloneError(
            "Unable to clone the GitHub repository. "
            "Confirm that the repository exists and is public."
        ) from exc

    commit_sha = repository.head.commit.hexsha

    return ClonedRepository(
        repository_id=repository_id,
        owner=owner,
        name=repository_name,
        local_path=local_path,
        commit_sha=commit_sha,
    )