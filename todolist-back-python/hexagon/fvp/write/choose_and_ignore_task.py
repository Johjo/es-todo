from dependencies import Dependencies
from hexagon.fvp.aggregate import FinalVersionPerfectedSession, FvpSessionSetPort
from hexagon.shared.type import TaskKey


class ChooseAndIgnoreTaskFvp:
    def __init__(self, set_of_fvp_sessions: FvpSessionSetPort):
        self.set_of_fvp_sessions = set_of_fvp_sessions

    def execute(self, chosen_task_id: TaskKey, ignored_task_id: TaskKey):
        session = self._get_or_create_session()

        session.choose_and_ignore_task(chosen_task_id, ignored_task_id)

        self._save(session)

    def _save(self, session):
        snapshot = session.to_snapshot()
        self.set_of_fvp_sessions.save(snapshot)

    def _get_or_create_session(self):
        snapshot = self.set_of_fvp_sessions.by()
        if snapshot:
            session = FinalVersionPerfectedSession.from_snapshot(snapshot)
        else:
            raise NotImplementedError()
        return session

    @classmethod
    def factory(cls, dependencies : Dependencies) -> 'ChooseAndIgnoreTaskFvp':
        return ChooseAndIgnoreTaskFvp(set_of_fvp_sessions=dependencies.get_adapter(FvpSessionSetPort))
