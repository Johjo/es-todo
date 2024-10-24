import pytest
from peewee import Database, SqliteDatabase

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from secondary.fvp.write.session_set_peewee import SessionPeewee, Session as DbSession
from test.secondary.fvp.test_session_repository_contract_testing import TestSessionRepositoryContractTesting


@pytest.fixture(autouse=True)
def peewee_database():
    database = SqliteDatabase(':memory:')
    database.connect()
    created_table = [DbSession]
    with database.bind_ctx(created_table):
        database.create_tables(created_table)
    return database


@pytest.fixture
def dependencies(peewee_database: Database) -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_adapter(FvpSessionSetPort, SessionPeewee.factory)
    dependencies = dependencies.feed_infrastructure(Database, lambda _: peewee_database)
    return dependencies



class TestSessionRepositoryPeewee(TestSessionRepositoryContractTesting):
    def feed(self, snapshot: FvpSnapshot) -> None:
        with self._database.bind_ctx([DbSession]):
            for ignored, chosen in snapshot.to_primitive_dict().items():
                DbSession.create(ignored=ignored, chosen=chosen)

    @pytest.fixture(autouse=True)
    def setup(self, peewee_database: Database, dependencies: Dependencies) -> None:
        self.dependencies = dependencies
        self._database = peewee_database

    def _create_sut(self) -> FvpSessionSetPort:
        return self.dependencies.get_adapter(FvpSessionSetPort)
