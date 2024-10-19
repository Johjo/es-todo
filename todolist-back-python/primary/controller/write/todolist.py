from hexagon.fvp.type import TaskKey
from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from hexagon.todolist.aggregate import TaskSnapshot
from hexagon.todolist.write.close_task import CloseTask
from hexagon.todolist.write.create_todolist import TodolistCreate
from hexagon.todolist.write.import_many_task import ImportManyTask
from hexagon.todolist.write.open_task import OpenTaskUseCase
from hexagon.todolist.write.reword_task import RewordTask
from dependencies import Dependencies
from test.secondary.todolist.test_external_todolist_markdown import MarkdownTodolist


class TodolistWriteController:
    def __init__(self, dependencies: Dependencies) -> None:
        self.dependencies = dependencies

    def create_todolist(self, todolist_name: str) -> None:
        use_case: TodolistCreate = self.dependencies.get_use_case(TodolistCreate)
        use_case.execute(todolist_name=todolist_name)

    def open_task(self, todolist_name: str, task_name: str):
        use_case: OpenTaskUseCase = self.dependencies.get_use_case(OpenTaskUseCase)
        use_case.execute(todolist_name=todolist_name, name=task_name)

    def close_task(self, todolist_name: str, task_key: TaskKey):
        use_case: CloseTask = self.dependencies.get_use_case(CloseTask)
        use_case.execute(todolist_name=todolist_name, key=task_key)

    def reword_task(self, todolist_name: str, task_key: TaskKey, new_name: str):
        use_case: RewordTask = self.dependencies.get_use_case(RewordTask)
        use_case.execute(todolist_name, task_key, new_name)

    def import_many_tasks_from_markdown(self, todolist_name: str, markdown: str):
        use_case: ImportManyTask = self.dependencies.get_use_case(ImportManyTask)
        external_todolist = MarkdownTodolist(markdown)
        use_case.execute(todolist_name, external_todolist)

    def choose_and_ignore_task(self, chosen_task: TaskKey, ignored_task: TaskKey):
        use_case : ChooseAndIgnoreTaskFvp = self.dependencies.get_use_case(ChooseAndIgnoreTaskFvp)
        use_case.execute(chosen_task_id=chosen_task, ignored_task_id=ignored_task)

