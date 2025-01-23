
from src.hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from src.secondary.fvp.simple_session_repository import FvpSessionSetInMemory
from test.secondary.fvp.write.base_test_session_set import BaseTestFvpSessionSet


class TestFvpSessionSet(BaseTestFvpSessionSet):
    def _create_sut(self) -> FvpSessionSetPort:
        self._sut = FvpSessionSetInMemory()
        return self._sut

    def feed(self, snapshot: FvpSnapshot) -> None:
        self._sut.feed(snapshot)
