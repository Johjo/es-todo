import pytest

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from src.secondary.fvp.simple_session_repository import FvpSessionSetInMemory
from test.secondary.fvp.write.base_test_session_set import BaseTestFvpSessionSet


class TestFvpSessionSet(BaseTestFvpSessionSet):
    @pytest.fixture(autouse=True)
    def before_each(self, sut: FvpSessionSetInMemory) -> None:
        self._sut = sut

    def feed(self, snapshot: FvpSnapshot) -> None:
        self._sut.feed(snapshot)

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        dependencies = Dependencies.create_empty()
        dependencies = dependencies.feed_adapter(FvpSessionSetPort, FvpSessionSetInMemory.factory)
        return dependencies
