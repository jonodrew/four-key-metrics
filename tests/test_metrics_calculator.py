import pytest

from four_key_metrics.metrics_calculator import MetricsCalculator
import functools


@pytest.fixture
def partial_add_deploy():
    return functools.partial(
        MetricsCalculator().add_deploy,
        **{"build_commit_hash": "12345", "last_build_commit_hash": "09876"}
    )


def test_can_calculate_metrics_for_nothing():
    calculator = MetricsCalculator()
    assert calculator.get_lead_time_mean_average() is None
    assert calculator.get_lead_time_standard_deviation() is None


def test_can_calculate_metrics_for_single_deploy_with_no_commits(partial_add_deploy):
    calculator = MetricsCalculator()
    calculator.add_deploy = partial_add_deploy

    calculator.add_deploy(build_timestamp=1, commits=[])

    assert calculator.get_lead_time_mean_average() is None
    assert calculator.get_lead_time_standard_deviation() is None


def test_can_calculate_metrics_for_one_deploy_with_one_commit(partial_add_deploy):
    calculator = MetricsCalculator()
    calculator.add_deploy = partial_add_deploy

    calculator.add_deploy(build_timestamp=1, commits=[0])

    assert calculator.get_lead_time_mean_average() == 1
    assert calculator.get_lead_time_standard_deviation() == 0


def test_can_calculate_metrics_for_one_deploy_with_two_commits(partial_add_deploy):
    calculator = MetricsCalculator()
    calculator.add_deploy = partial_add_deploy

    calculator.add_deploy(build_timestamp=10, commits=[8, 8])

    assert calculator.get_lead_time_mean_average() == 2
    assert calculator.get_lead_time_standard_deviation() == 0


def test_can_calculate_metrics_for_two_deploys_with_two_commits(partial_add_deploy):
    calculator = MetricsCalculator()
    calculator.add_deploy = partial_add_deploy

    calculator.add_deploy(build_timestamp=10, commits=[8, 8])
    calculator.add_deploy(build_timestamp=20, commits=[9, 9])

    assert calculator.get_lead_time_mean_average() == 6.5
    assert calculator.get_lead_time_standard_deviation() == 4.5
