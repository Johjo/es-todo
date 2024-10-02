from abc import ABC, abstractmethod

from hexagon.fvp.domain_model import Task, FinalVersionPerfectedSession, NothingToDo, DoTheTask, ChooseTheTask
from hexagon.fvp.port import FvpSessionRepository


class TaskReader(ABC):
    @abstractmethod
    def all(self) -> list[Task]:
        pass


class WhichTaskQueryContract(ABC):
    @abstractmethod
    def which_task(self) -> NothingToDo | DoTheTask | ChooseTheTask:
        pass


class WhichTaskQuery(WhichTaskQueryContract):
    def __init__(self, set_of_open_tasks: TaskReader, set_of_fvp_sessions: FvpSessionRepository):
        self.set_of_fvp_sessions = set_of_fvp_sessions
        self.set_of_open_tasks = set_of_open_tasks

    def which_task(self):
        session = self._get_or_create_session()
        return session.which_task(self.set_of_open_tasks.all())

    def _get_or_create_session(self):
        snapshot = self.set_of_fvp_sessions.by()
        if snapshot:
            session = FinalVersionPerfectedSession.from_snapshot(snapshot)
        else:
            session = FinalVersionPerfectedSession.create()
        return session
