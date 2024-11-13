import pytest
from peewee import Database, SqliteDatabase

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from infra.peewee.sdk import PeeweeSdk, FvpSession as FvpSessionSdk
from secondary.fvp.write.session_set_peewee import SessionPeewee
from test.secondary.fvp.test_session_repository_contract_testing import TestSessionRepositoryContractTesting


@pytest.fixture()
def peewee_database():
    database = SqliteDatabase(':memory:')
    database.connect()
    sdk = PeeweeSdk(database)
    sdk.create_tables()
    return database


@pytest.fixture
def dependencies(peewee_database: Database) -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_adapter(FvpSessionSetPort, SessionPeewee.factory)
    dependencies = dependencies.feed_infrastructure(Database, lambda _: peewee_database)
    return dependencies



class TestSessionRepositoryPeewee(TestSessionRepositoryContractTesting):
    def feed(self, session: FvpSnapshot) -> None:
        sdk = PeeweeSdk(self._database)
        sdk.upsert_fvp_session(
            FvpSessionSdk(priorities=[(ignored, chosen) for ignored, chosen in session.task_priorities.items()]))

    @pytest.fixture(autouse=True)
    def setup(self, peewee_database: Database, dependencies: Dependencies) -> None:
        self.dependencies = dependencies
        self._database = peewee_database

    def _create_sut(self) -> FvpSessionSetPort:
        return self.dependencies.get_adapter(FvpSessionSetPort)
