import httpretty
import json

from four_key_metrics.github import get_commits_between


def test_can_get_comparison_with_one_commit():
    github_response = {
        "commits": [
            {
                "commit": {
                    "author": {
                        "date": "2021-09-17T13:30:45Z"
                    }
                }
            }
        ]
    }

    httpretty.enable(allow_net_connect=False, verbose=True)
    httpretty.register_uri(
        httpretty.GET,
        "https://api.github.com/repos/uktrade/data-hub-frontend/compare/v9.19.0...v9.17.1",
        body=json.dumps(github_response)
    )

    commits = get_commits_between("uktrade", "data-hub-frontend", "v9.19.0", "v9.17.1")

    assert len(commits) == 1
    assert commits[0].timestamp == 1631885445.0


def test_can_get_comparison_with_two_commits():
    github_response = {
        "commits": [
            {
                "commit": {
                    "author": {
                        "date": "2021-09-17T13:30:45Z"
                    }
                }
            },
            {
                "commit": {
                    "author": {
                        "date": "2021-09-18T13:31:45Z"
                    }
                }
            }
        ]
    }

    httpretty.enable(allow_net_connect=False, verbose=True)
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

    httpretty.enable(allow_net_connect=False, verbose=True)
    httpretty.register_uri(
        httpretty.GET,
        "https://api.github.com/repos/123/456/compare/789...0",
        body=json.dumps(github_response)
    )

    get_commits_between("123", "456", "789", "0")

    assert httpretty.last_request().url == 'https://api.github.com/repos/123/456/compare/789...0'
