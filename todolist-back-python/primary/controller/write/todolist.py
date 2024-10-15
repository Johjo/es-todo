from domain.todo.todoapp import TodoApp
from hexagon.todolist.aggregate import TaskKey, TaskSnapshot
from hexagon.todolist.write.close_task import CloseTask
from hexagon.todolist.write.create_todolist import TodolistCreate
from hexagon.todolist.write.import_many_task import ImportManyTask
from hexagon.todolist.write.open_task import OpenTaskUseCase
from hexagon.todolist.write.reword_task import RewordTask
from primary.controller.write.dependencies import Dependencies


def create_todolist(name):
    app = TodoApp()
    app.start_todolist(name)


class TodolistWriteController:
    def __init__(self, dependencies: Dependencies) -> None:
        self.dependencies = dependencies

    def create_todolist(self, todolist_name: str) -> None:
        use_case: TodolistCreate = self.dependencies.get_use_case(TodolistCreate)
        use_case.execute(todolist_name=todolist_name)

    def open_task(self, todolist_name: str, task_name: str):
        use_case: OpenTaskUseCase = self.dependencies.get_use_case(OpenTaskUseCase)
        use_case.execute(todolist_name=todolist_name, name=task_name)

    def close_task(self, todolist_name: str, task_key: int):
        use_case: CloseTask = self.dependencies.get_use_case(CloseTask)
        use_case.execute(todolist_name=todolist_name, key=TaskKey(task_key))

    def reword_task(self, todolist_name: str, task_key: int, new_name: str):
        use_case: RewordTask = self.dependencies.get_use_case(RewordTask)
        use_case.execute(todolist_name, TaskKey(task_key), new_name)

    def import_many_tasks(self, tasks: list[TaskSnapshot], todolist_name: str):
        use_case: ImportManyTask = self.dependencies.get_use_case(ImportManyTask)
        use_case.execute(todolist_name, tasks)
