from typing import final

from hexagon.fvp.domain_model import FvpSnapshot
from hexagon.fvp.port import FvpSessionRepository
from secondary.fvp.simple_session_repository import SimpleSessionRepository
from test.secondary.fvp.test_session_repository_contract_testing import TestSessionRepositoryContractTesting


class TestSimpleSessionRepository(TestSessionRepositoryContractTesting):
    def _create_sut(self) -> FvpSessionRepository:
        self._sut = SimpleSessionRepository()
        return self._sut

    def feed(self, snapshot: FvpSnapshot) -> None:
        self._sut.feed(snapshot)
