from unittest.mock import patch, Mock

from four_key_metrics.build import Build
from four_key_metrics.github import GitCommit


@patch("four_key_metrics.build.requests", return_value=Mock())
def test_build_get_commits(mock_github):
    """
    This tests whether a build object can get all of its commits. It Mocks the request to GitHub to allow us to try
    different responses
    """
    build = Build(0, 1, True, "test", "abcdef")
    build.get_commits_between()
    assert build.commits == [GitCommit("abcdef")]
