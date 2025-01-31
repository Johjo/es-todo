import sqlite3

import pytest
from typing_extensions import override

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from src.hexagon.shared.type import UserKey
from src.infra.sqlite.sdk import SqliteSdk
from src.infra.sqlite.type import FvpSession as FvpSessionSdk
from src.secondary.fvp.write.session_set_sqlite import SessionSqlite
from test.secondary.fvp.write.base_test_session_set import BaseTestFvpSessionSet


@pytest.fixture()
def connection():
    connection = sqlite3.connect(':memory:')
    sdk = SqliteSdk(connection)
    sdk.create_tables()
    return connection


class TestFvpSessionSetSqlite(BaseTestFvpSessionSet):
    @pytest.fixture(autouse=True)
    def before_each(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def feed(self, user_key: str, snapshot: FvpSnapshot) -> None:
        sdk = SqliteSdk(self._connection)
        sdk.upsert_fvp_session(user_key=user_key,
            fvp_session=FvpSessionSdk(priorities=[(ignored, chosen) for ignored, chosen in snapshot.task_priorities.items()]))

    @pytest.fixture
    def dependencies(self) -> Dependencies:
        dependencies = Dependencies.create_empty()
        dependencies = dependencies.feed_adapter(FvpSessionSetPort, SessionSqlite.factory)
        dependencies = dependencies.feed_infrastructure(sqlite3.Connection, lambda _: self._connection)
        return dependencies
