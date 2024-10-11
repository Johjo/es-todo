from domain.todo.todoapp import TodoApp
from hexagon.todolist.write.create_todolist import TodolistCreate
from hexagon.todolist.write.open_task import OpenTask
from primary.controller.write.dependencies import Dependencies


def create_todolist(name):
    app = TodoApp()
    app.start_todolist(name)


class TodolistWriteController:
    def __init__(self, dependencies: Dependencies) -> None:
        self.dependencies = dependencies

    def create_todolist(self, todolist_name):
        todolist_create = self.dependencies.get_use_case(TodolistCreate)
        todolist_create.execute(todolist_name=todolist_name)

    def open_task(self, dependencies, task_key, task_name, todolist_name):
        use_case = dependencies.get_use_case(OpenTask)
        use_case.execute(todolist_name=todolist_name, key=task_key, name=task_name)

