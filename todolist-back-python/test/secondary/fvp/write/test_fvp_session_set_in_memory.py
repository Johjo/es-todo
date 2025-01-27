import pytest

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from src.infra.fvp_memory import FvpMemory
from src.secondary.fvp.write.fvp_session_set_in_memory import FvpSessionSetInMemory
from test.secondary.fvp.write.base_test_session_set import BaseTestFvpSessionSet


class TestFvpSessionSetInMemory(BaseTestFvpSessionSet):
    @pytest.fixture(autouse=True)
    def before_each(self) -> None:
        self._fvp_memory = FvpMemory()

    def feed(self, snapshot: FvpSnapshot) -> None:
        self._fvp_memory.feed(snapshot)

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        dependencies = Dependencies.create_empty()
        dependencies = dependencies.feed_adapter(FvpSessionSetPort, FvpSessionSetInMemory.factory)
        dependencies = dependencies.feed_infrastructure(FvpMemory, lambda _: self._fvp_memory)
        return dependencies
