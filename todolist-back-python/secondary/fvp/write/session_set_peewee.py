from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSessionSetPort, FvpSnapshot


class SessionPeewee(FvpSessionSetPort):
    def save(self, snapshot: FvpSnapshot) -> None:
        raise NotImplementedError()

    def by(self) -> FvpSnapshot | None:
        raise NotImplementedError()

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'SessionPeewee':
        return SessionPeewee()