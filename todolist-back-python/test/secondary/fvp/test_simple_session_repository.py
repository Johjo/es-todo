from typing import final

from hexagon.fvp.domain_model import FvpSnapshot
from hexagon.fvp.port import FvpSessionSetPort
from secondary.fvp.simple_session_repository import FvpSessionSetForTest
from test.secondary.fvp.test_session_repository_contract_testing import TestSessionRepositoryContractTesting


class TestSimpleSessionRepository(TestSessionRepositoryContractTesting):
    def _create_sut(self) -> FvpSessionSetPort:
        self._sut = FvpSessionSetForTest()
        return self._sut

    def feed(self, snapshot: FvpSnapshot) -> None:
        self._sut.feed(snapshot)
