from domain.todo.todoapp import TodoApp
from hexagon.todolist.aggregate import TaskKey
from hexagon.todolist.write.close_task import CloseTask
from hexagon.todolist.write.create_todolist import TodolistCreate
from hexagon.todolist.write.open_task import OpenTask
from hexagon.todolist.write.reword_task import RewordTask
from primary.controller.write.dependencies import Dependencies


def create_todolist(name):
    app = TodoApp()
    app.start_todolist(name)


class TodolistWriteController:
    def __init__(self, dependencies: Dependencies) -> None:
        self.dependencies = dependencies

    def create_todolist(self, todolist_name: str) -> None:
        todolist_create = self.dependencies.get_use_case(TodolistCreate)
        todolist_create.execute(todolist_name=todolist_name)

    def open_task(self, todolist_name: str, task_key: int, task_name: str):
        use_case = self.dependencies.get_use_case(OpenTask)
        use_case.execute(todolist_name=todolist_name, key=TaskKey(task_key), name=task_name)

    def close_task(self, todolist_name: str, task_key: int):
        use_case = self.dependencies.get_use_case(CloseTask)
        use_case.execute(todolist_name=todolist_name, key=TaskKey(task_key))

    def reword_task(self, new_name, task_key, todolist_name):
        use_case = self.dependencies.get_use_case(RewordTask)
        use_case.execute(todolist_name, TaskKey(task_key), new_name)
