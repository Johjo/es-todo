from hexagon.fvp.aggregate import FinalVersionPerfectedSession
from hexagon.fvp.type import TaskKey
from test.hexagon.fvp.write.fixture import FvpSessionSetForTest


class CancelPriorityFvp:
    def __init__(self, session_set: FvpSessionSetForTest):
        self._session_set = session_set

    def execute(self, task_key: TaskKey):
        session_snapshot = self._session_set.by()
        session = FinalVersionPerfectedSession.from_snapshot(session_snapshot)
        session.cancel_priority(task_key)

        self._session_set.save(session.to_snapshot())
