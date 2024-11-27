
from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from secondary.fvp.simple_session_repository import FvpSessionSetForTest
from test.secondary.fvp.write.base_test_session_set import BaseTestSessionSet


class TestSimpleSessionSet(BaseTestSessionSet):
    def _create_sut(self) -> FvpSessionSetPort:
        self._sut = FvpSessionSetForTest()
        return self._sut

    def feed(self, snapshot: FvpSnapshot) -> None:
        self._sut.feed(snapshot)
