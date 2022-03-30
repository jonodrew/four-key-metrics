import os
from dataclasses import dataclass
import ciso8601
import requests


@dataclass
class GitCommit:
    sha: str
    timestamp: float = 0.0


def get_commits_between(organisation, repository, base, head):
    response = requests.get(
        "https://api.github.com/repos/%s/%s/compare/%s...%s"
        % (organisation, repository, base, head),
        auth=(os.environ["GITHUB_USERNAME"], os.environ["GITHUB_TOKEN"]),
        headers={"Accept": "application/vnd.github.v3+json"},
        timeout=30,
    )

    commits = []

    for commit in response.json()["commits"]:
        commit = commit["commit"]
        commit_author_date = commit["author"]["date"]
        timestamp = ciso8601.parse_datetime(commit_author_date).timestamp()
        commits.append(GitCommit(sha=commit["sha"], timestamp=timestamp))
    return commits
