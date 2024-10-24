from peewee import Database, Model, UUIDField

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSessionSetPort, FvpSnapshot


class Session(Model):
    ignored = UUIDField()
    chosen = UUIDField()


class SessionPeewee(FvpSessionSetPort):
    def __init__(self, database: Database):
        self._database : Database = database

    def save(self, snapshot: FvpSnapshot) -> None:
        with self._database.bind_ctx([Session]):
            Session.delete().execute()
            for ignored, chosen in snapshot.to_primitive_dict().items():
                Session.create(ignored=ignored, chosen=chosen)

    def by(self) -> FvpSnapshot | None:
        with self._database.bind_ctx([Session]):
            return FvpSnapshot.from_primitive_dict({session.ignored: session.chosen for session in Session.select()})


        pass

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'SessionPeewee':
        return SessionPeewee(dependencies.get_infrastructure(Database))