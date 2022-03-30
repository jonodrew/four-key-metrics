import os

import ciso8601
import requests

from four_key_metrics.github import GitCommit


class Build:
    """
    A build is a collection of commits that is turned into a binary, ready to become a deployment
    """
    def __init__(self, started_at, finished_at, successful, environment, git_reference):
        self.started_at = started_at
        self.finished_at = finished_at
        self.successful = successful
        self.environment = environment
        self.git_reference = git_reference
        self.commits = None

    def get_commits_between(self, organisation, repository, base, head):
        response = requests.get(
            f"https://api.github.com/repos/{organisation}/{repository}/compare/{base}...{head}",
            auth=(os.environ["GITHUB_USERNAME"], os.environ["GITHUB_TOKEN"]),
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=30,
        )

        for commit in response.json()["commits"]:
            commit = commit["commit"]
            commit_author_date = commit["author"]["date"]
            timestamp = ciso8601.parse_datetime(commit_author_date).timestamp()
            self.commits.append(GitCommit(sha=commit["sha"], timestamp=timestamp))
            # could you work out the lead time of each commit here, by comparing with self.started_at?
            # if not, is self.started_at only important to calculate build time?

