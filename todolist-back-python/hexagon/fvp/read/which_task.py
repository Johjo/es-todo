from abc import ABC, abstractmethod
from dataclasses import dataclass

from dependencies import Dependencies
from hexagon.fvp.aggregate import Task, FinalVersionPerfectedSession, NothingToDo, DoTheTask, ChooseTheTask, \
    FvpSessionSetPort
from hexagon.shared.type import TodolistName


@dataclass(frozen=True, eq=True)
class TaskFilter:
    todolist_name: TodolistName
    include_context: tuple[str, ...] = ()
    exclude_context: tuple[str, ...] = ()

    def include(self, task_name: str) -> bool:
        if not self.match_included_context(task_name):
            return False

        if self.match_excluded_context(task_name):
            return False

        return True

    def match_included_context(self, task_name: str) -> bool:
        if self.include_context == ():
            return True

        for context in self.include_context:
            if any(context == word for word in task_name.split()):
                return True
        return False


    def match_excluded_context(self, task_name: str) -> bool:
        for context in self.exclude_context:
            if any(context == word for word in task_name.split()):
                return True
        return False


class TodolistPort(ABC):
    @abstractmethod
    def all_open_tasks(self, task_filter: TaskFilter) -> list[Task]:
        pass


class WhichTaskQuery:
    def __init__(self, todolist: TodolistPort, fvp_sessions_set: FvpSessionSetPort):
        self._fvp_sessions_set = fvp_sessions_set
        self._todolist = todolist

    def which_task(self, task_filter: TaskFilter) -> NothingToDo | DoTheTask | ChooseTheTask:
        session : FinalVersionPerfectedSession= self._get_or_create_session()
        open_tasks = self._todolist.all_open_tasks(task_filter)
        return session.which_task(open_tasks)

    # todo: rendre ça plus fonctionnel
    def _get_or_create_session(self) -> FinalVersionPerfectedSession:
        snapshot = self._fvp_sessions_set.by()
        if snapshot:
            session = FinalVersionPerfectedSession.from_snapshot(snapshot)
        else:
            session = FinalVersionPerfectedSession.create()
        return session

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'WhichTaskQuery':
        return WhichTaskQuery(dependencies.get_adapter(TodolistPort), dependencies.get_adapter(FvpSessionSetPort))

