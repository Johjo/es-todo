import sqlite3

import pytest

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from src.infra.sqlite.sdk import SqliteSdk
from src.infra.sqlite.type import FvpSession as FvpSessionSdk
from src.secondary.fvp.write.session_set_sqlite import SessionSqlite
from test.secondary.fvp.write.base_test_session_set import BaseTestSessionSet


@pytest.fixture()
def connection():
    connection = sqlite3.connect(':memory:')
    sdk = SqliteSdk(connection)
    sdk.create_tables()
    return connection


@pytest.fixture
def dependencies(connection: sqlite3.Connection) -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_adapter(FvpSessionSetPort, SessionSqlite.factory)
    dependencies = dependencies.feed_infrastructure(sqlite3.Connection, lambda _: connection)
    return dependencies



class TestSessionSetSqlite(BaseTestSessionSet):
    def feed(self, session: FvpSnapshot) -> None:
        sdk = SqliteSdk(self._connection)
        sdk.upsert_fvp_session(
            FvpSessionSdk(priorities=[(ignored, chosen) for ignored, chosen in session.task_priorities.items()]))

    @pytest.fixture(autouse=True)
    def setup(self, connection: sqlite3.Connection, dependencies: Dependencies) -> None:
        self.dependencies = dependencies
        self._connection = connection

    def _create_sut(self) -> FvpSessionSetPort:
        return self.dependencies.get_adapter(FvpSessionSetPort)
