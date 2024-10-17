import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeAlias, NewType

from hexagon.fvp.aggregate import Task, FinalVersionPerfectedSession, NothingToDo, DoTheTask, ChooseTheTask, \
    FvpSessionSetPort


@dataclass(frozen=True)
class TaskFilter:
    todolist_name: str


class TodolistPort(ABC):
    @abstractmethod
    def all_open_tasks(self, task_filter: TaskFilter) -> list[Task]:
        pass


# todo: faire disparaître ce contrat
class WhichTaskQueryContract(ABC):
    @abstractmethod
    def which_task(self, task_filter: TaskFilter) -> NothingToDo | DoTheTask | ChooseTheTask:
        pass


class WhichTaskQuery(WhichTaskQueryContract):
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

