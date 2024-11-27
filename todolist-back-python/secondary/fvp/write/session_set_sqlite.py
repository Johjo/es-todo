import sqlite3


from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSessionSetPort, FvpSnapshot
from hexagon.shared.type import TaskKey
from infra.sqlite.sdk import SqliteSdk
from infra.sqlite.type import FvpSession as FvpSessionSdk


class SessionSqlite(FvpSessionSetPort):
    def __init__(self, connection: sqlite3.Connection):
        self._sdk = SqliteSdk(connection)

    def save(self, session: FvpSnapshot) -> None:
        self._sdk.upsert_fvp_session(
            FvpSessionSdk(priorities=[(ignored, chosen) for ignored, chosen in session.task_priorities.items()]))

    def by(self) -> FvpSnapshot:
        session : FvpSessionSdk = self._sdk.fvp_session_by()
        return FvpSnapshot.from_primitive_dict({TaskKey(ignored): TaskKey(chosen) for (ignored, chosen) in session.priorities})

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'SessionSqlite':
        return SessionSqlite(dependencies.get_infrastructure(sqlite3.Connection))