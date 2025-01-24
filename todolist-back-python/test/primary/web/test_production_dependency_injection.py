import pytest
from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore

from src.dependencies import Dependencies
from src.shared.const import USER_KEY
from start_web_for_test import inject_all_dependencies


@pytest.fixture
def sut() -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_path("sqlite_database_path", lambda _: ":memory:")
    dependencies = dependencies.feed_data(data_name=USER_KEY, value="any value")
    dependencies = inject_all_dependencies(dependencies)
    return dependencies

def test_describe_dependencies(sut: Dependencies) -> None:
    verify(sut.describe(), reporter=PythonNativeReporter())