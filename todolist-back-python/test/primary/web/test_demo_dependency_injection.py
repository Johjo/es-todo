import pytest
from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore

from dependencies import Dependencies
from primary.demo_dependencies import inject_all_dependencies
from shared.const import USER_KEY


@pytest.fixture
def sut() -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = inject_all_dependencies(dependencies)
    dependencies = dependencies.feed_data(data_name=USER_KEY, value="test")
    return dependencies


def test_describe_dependencies(sut: Dependencies) -> None:
    verify(sut.describe(), reporter=PythonNativeReporter())
