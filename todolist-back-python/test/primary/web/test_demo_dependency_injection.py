import pytest
from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore

from src.dependencies import Dependencies
from src.primary.demo_dependencies import inject_all_dependencies


@pytest.fixture
def sut() -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = inject_all_dependencies(dependencies)
    return dependencies


def test_describe_dependencies(sut: Dependencies) -> None:
    verify(sut.describe(), reporter=PythonNativeReporter())
