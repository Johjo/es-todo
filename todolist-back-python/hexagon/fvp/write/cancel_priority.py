from dependencies import Dependencies
from hexagon.fvp.aggregate import FinalVersionPerfectedSession, FvpSessionSetPort
from hexagon.shared.type import TaskKey


class CancelPriority:
    def __init__(self, session_set: FvpSessionSetPort):
        self._session_set = session_set

    def execute(self, task_key: TaskKey):
        session_snapshot = self._session_set.by()
        session = FinalVersionPerfectedSession.from_snapshot(session_snapshot)
        session.cancel_priority(task_key)

        self._session_set.save(session.to_snapshot())

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'CancelPriority':
        return CancelPriority(dependencies.get_adapter(FvpSessionSetPort))