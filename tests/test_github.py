import json
import os
from typing import Callable, Dict, Optional

import httpretty
import pytest

from four_key_metrics.github import get_commits_between
from tests.authorization_assertions import assert_authorization_is


@pytest.fixture
def commit_dict() -> Callable[[Optional[str], Optional[str]], Dict]:
    def _commit_dict(sha="abcdef", timestamp: str = "2021-09-17T13:30:45Z"):
        return {
            "commit": {
                "sha": sha,
                "author": {
                    "date": timestamp
                }
            }
        }
    return _commit_dict


@pytest.fixture(autouse=True)
def around_each():
    httpretty.enable(allow_net_connect=False, verbose=True)
    os.environ['GITHUB_USERNAME'] = 'testing'
    os.environ['GITHUB_TOKEN'] = '5678'
    yield
    httpretty.reset()
    httpretty.disable()


def test_can_get_comparison_with_one_commit(commit_dict):
    github_response = {
        "commits": [
            commit_dict()
        ]
    }

    httpretty.register_uri(
        httpretty.GET,
        "https://api.github.com/repos/uktrade/data-hub-frontend/compare/v9.19.0...v9.17.1",
        body=json.dumps(github_response)
    )

    commits = get_commits_between("uktrade", "data-hub-frontend", "v9.19.0", "v9.17.1")

    assert len(commits) == 1
    assert commits[0].timestamp == 1631885445.0


def test_can_get_comparison_with_two_commits(commit_dict):
    github_response = {
        "commits": [
            commit_dict(),
            commit_dict("12345", "2021-09-18T13:31:45Z")
        ]
    }

    httpretty.register_uri(
        httpretty.GET,
        "https://api.github.com/repos/uktrade/data-hub-frontend/compare/v9.19.0...v9.17.1",
        body=json.dumps(github_response)
    )

    commits = get_commits_between("uktrade", "data-hub-frontend", "v9.19.0", "v9.17.1")

    assert len(commits) == 2
    assert commits[0].timestamp == 1631885445.0
    assert commits[1].timestamp == 1631971905.0


def test_can_request_different_comparisons():
    github_response = {
        "commits": []
    }

    httpretty.register_uri(
        httpretty.GET,
        "https://api.github.com/repos/123/456/compare/789...0",
        body=json.dumps(github_response)
    )

    get_commits_between("123", "456", "789", "0")

    assert httpretty.last_request().url == 'https://api.github.com/repos/123/456/compare/789...0'


def test_can_use_authentication():
    github_response = {
        "commits": []
    }

    httpretty.register_uri(
        httpretty.GET,
        "https://api.github.com/repos/123/456/compare/789...0",
        body=json.dumps(github_response)
    )

    get_commits_between("123", "456", "789", "0")

    assert_authorization_is(b'testing:5678')
