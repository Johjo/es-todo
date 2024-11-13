from peewee import Database  # type: ignore

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSessionSetPort, FvpSnapshot
from hexagon.shared.type import TaskKey
from infra.peewee.sdk import PeeweeSdk, FvpSession as FvpSessionSdk


class SessionPeewee(FvpSessionSetPort):
    def __init__(self, database: Database):
        self._database : Database = database
        self._sdk = PeeweeSdk(database)

    def save(self, session: FvpSnapshot) -> None:
        self._sdk.upsert_fvp_session(
            FvpSessionSdk(priorities=[(ignored, chosen) for ignored, chosen in session.task_priorities.items()]))

    def by(self) -> FvpSnapshot:
        session : FvpSessionSdk = self._sdk.fvp_session_by()
        return FvpSnapshot.from_primitive_dict({TaskKey(ignored): TaskKey(chosen) for (ignored, chosen) in session.priorities})

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'SessionPeewee':
        return SessionPeewee(dependencies.get_infrastructure(Database))