from dataclasses import dataclass
from uuid import UUID, uuid4

from domain.todo.todoapp import TodoApp
from hexagon.fvp.domain_model import NothingToDo, DoTheTask, ChooseTheTask
from hexagon.fvp.read.which_task import WhichTaskQuery
from hexagon.query.context_query import TodoContextQuery
from hexagon.todolist.aggregate import TodolistSetPort
from primary.controller.dependency_list import DependencyList
from primary.controller.read.current_contexts import OpenTaskReaderApp
from primary.controller.write.dependencies import Dependencies


@dataclass
class Task:
    id: UUID
    name: str

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name
        }

@dataclass
class TodoList:
    tasks: list[Task]
    number_of_tasks: int
    contexts: list[str]

    def __post_init__(self):
        assert len(self.tasks) <= 2, "Todolist can only have 2 tasks to examine at most"

    def to_dict(self):
        return {
            "tasks": [task.to_dict() for task in self.tasks],
            "numberOfTasks": self.number_of_tasks,
            "contexts": self.contexts
        }


def todolist(todolist_name, dependencies: DependencyList) -> TodoList:
    return TodoList(tasks=get_tasks(dependencies, todolist_name),
                    number_of_tasks=get_number_of_tasks(todolist_name),
                    contexts=get_all_contexts(todolist_name))


def get_number_of_tasks(todolist_name):
    app = TodoApp()
    todolist_id = app.open_todolist(todolist_name)
    number_of_items = len(app.get_open_items(todolist_id))
    return number_of_items


def get_tasks(dependencies, todolist_name):
    set_of_open_tasks = dependencies.task_reader_for_fvp_which_task(todolist_name=todolist_name, only_inbox=False,
                                                                    context="")
    set_of_fvp_sessions = dependencies.fvp_session_repository_for_fvp()
    response = WhichTaskQuery(todolist=set_of_open_tasks, fvp_sessions_set=set_of_fvp_sessions).which_task()
    tasks = []
    match response:
        case DoTheTask(id=task_id, name=task_name):
            tasks.append(Task(id=task_id, name=task_name))
        case ChooseTheTask(id_1=index_1, name_1=name_1, id_2=index_2, name_2=name_2):
            tasks.append(Task(id=index_1, name=name_1))
            tasks.append(Task(id=index_2, name=name_2))
    return tasks


def get_all_contexts(todolist_name):
    task_reader = OpenTaskReaderApp(todolist_name)
    all_contexts = [context for context in TodoContextQuery(task_reader).all_contexts().keys()]
    return all_contexts


class TodolistReadController:
    def __init__(self, dependencies: Dependencies):
        self.dependencies = dependencies

    def all_todolist_by_name(self) -> list[str]:
        todolist_set = self.dependencies.get_adapter(TodolistSetPort)
        return todolist_set.all_by_name()
