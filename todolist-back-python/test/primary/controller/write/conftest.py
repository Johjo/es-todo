import pytest

from primary.controller.write.dependencies import Dependencies, inject_use_cases


@pytest.fixture
def empty_dependencies():
    return Dependencies.create_empty()


@pytest.fixture
def dependencies_with_use_cases():
    return inject_use_cases(Dependencies.create_empty())
