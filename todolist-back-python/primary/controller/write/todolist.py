from dependencies import Dependencies
from hexagon.fvp.write.reset_fvp_session import ResetFvpSession
from hexagon.shared.type import TaskKey, TodolistName, TaskExecutionDate
from hexagon.fvp.write.cancel_priority import CancelPriority as Fvp_CancelPriority
from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from hexagon.todolist.write.close_task import CloseTask
from hexagon.todolist.write.create_todolist import TodolistCreate
from hexagon.todolist.write.import_many_task import ImportManyTask
from hexagon.todolist.write.open_task import OpenTaskUseCase
from hexagon.todolist.write.postpone_task import PostPoneTask
from hexagon.todolist.write.reword_task import RewordTask
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
        use_case: ChooseAndIgnoreTaskFvp = self.dependencies.get_use_case(ChooseAndIgnoreTaskFvp)
        use_case.execute(chosen_task_id=chosen_task, ignored_task_id=ignored_task)

    def cancel_priority(self, task_key: TaskKey):
        use_case: Fvp_CancelPriority = self.dependencies.get_use_case(Fvp_CancelPriority)
        use_case.execute(task_key)

    def reset_all_priorities(self) -> None:
        use_case: ResetFvpSession = self.dependencies.get_use_case(ResetFvpSession)
        use_case.execute()

    def postpone_task(self, name: TodolistName, key: TaskKey, execution_date: TaskExecutionDate):
        use_case: PostPoneTask = self.dependencies.get_use_case(PostPoneTask)
        use_case.execute(todolist_name=name, key=key, execution_date=execution_date)
