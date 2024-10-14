from abc import ABC, abstractmethod

from hexagon.fvp.domain_model import NothingToDo, DoTheTask, ChooseTheTask
from hexagon.fvp.port import FvpSessionSetPort
from hexagon.fvp.read.which_task import WhichTaskQueryContract, WhichTaskQuery, TodolistPort
from utils import SharedInstanceBuiltIn


# todo : remove this
class DependencyList(ABC):
    def which_task_query(self, todolist_name: str, only_inbox: bool, context: str) -> WhichTaskQueryContract:
        set_of_open_tasks = self.task_reader_for_which_task_query(todolist_name=todolist_name,
                                                                  only_inbox=only_inbox,
                                                                  context=context)
        set_of_fvp_sessions = self.fvp_session_repository_for_which_task_query()
        return WhichTaskQuery(todolist=set_of_open_tasks, fvp_sessions_set=set_of_fvp_sessions)

    @abstractmethod
    def task_reader_for_which_task_query(self, todolist_name: str, only_inbox: bool, context: str) -> TodolistPort:
        pass

    @abstractmethod
    def fvp_session_repository_for_which_task_query(self) -> FvpSessionSetPort:
        pass


def which_task(dependencies, todolist_name: str, only_inbox: bool, context: str) -> dict:
    query: WhichTaskQueryContract = dependencies.which_task_query(todolist_name=todolist_name,
                                                                  only_inbox=only_inbox,
                                                                  context=context)
    match query.which_task():
        case NothingToDo():
            return {"fvpTasks": []}
        case DoTheTask(id=task_id, name=name):
            return {"fvpTasks": [{"id": task_id, "name": name}]}
        case ChooseTheTask(id_1=task_id_1, name_1=name_1, id_2=task_id_2, name_2=name_2):
            return {"fvpTasks": [{"id": task_id_1, "name": name_1}, {"id": task_id_2, "name": name_2}]}
