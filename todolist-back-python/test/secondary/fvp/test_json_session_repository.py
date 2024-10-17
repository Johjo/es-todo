import json
import os
from pathlib import Path

import pytest

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from infra.json_file import JsonFile
from secondary.fvp.json_session_repository import JsonSessionRepository
from test.secondary.fvp.test_session_repository_contract_testing import TestSessionRepositoryContractTesting

@pytest.fixture
def json_path(tmp_path: Path) -> Path:
    return tmp_path / "session_fvp.json"


@pytest.fixture
def dependencies(json_path: Path) -> Dependencies:
    return Dependencies.create_empty()


class TestJsonSessionRepository(TestSessionRepositoryContractTesting):
    def feed(self, snapshot: FvpSnapshot) -> None:
        self._json_file = JsonFile(self.path)
        self._json_file.insert("all", snapshot.to_primitive_dict())

    @pytest.fixture(autouse=True)
    def setup(self, json_path: Path, dependencies: Dependencies) -> None:
        self.path = json_path
        dependencies = dependencies.feed_path("session_fvp_json_path", lambda _: self.path)
        dependencies = dependencies.feed_adapter(FvpSessionSetPort, JsonSessionRepository.factory)
        self.dependencies = dependencies

    def _create_sut(self) -> FvpSessionSetPort:
        return self.dependencies.get_adapter(FvpSessionSetPort)




