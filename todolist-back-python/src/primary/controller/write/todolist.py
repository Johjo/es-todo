from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from src.dependencies import Dependencies
from src.hexagon.fvp.write.reset_fvp_session import ResetFvpSession
from src.hexagon.shared.type import TaskKey, TodolistName, TaskExecutionDate, TaskName
from src.hexagon.fvp.write.cancel_priority import CancelPriority as Fvp_CancelPriority
from src.hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from src.hexagon.todolist.write.close_task import CloseTask
from src.hexagon.todolist.write.create_todolist import TodolistCreate
from src.hexagon.todolist.write.import_many_task import ImportManyTask
from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from src.hexagon.todolist.write.postpone_task import PostPoneTask
from src.hexagon.todolist.write.reword_task import RewordTask
from src.secondary.todolist.markdown_todolist import MarkdownTodolist


class DateTimeProviderPort(ABC):
    @abstractmethod
    def now(self) -> datetime:
        pass


class TodolistWriteController:
    def __init__(self, dependencies: Dependencies) -> None:
        self.dependencies = dependencies
        self._datetime_provider = dependencies.get_adapter(DateTimeProviderPort)


    def create_todolist(self, todolist_name: TodolistName) -> None:
        use_case: TodolistCreate = self.dependencies.get_use_case(TodolistCreate)
        use_case.execute(todolist_name=todolist_name)

    def open_task(self, todolist_name: TodolistName, task_name: TaskName):
        use_case: OpenTaskUseCase = self.dependencies.get_use_case(OpenTaskUseCase)
        use_case.execute(todolist_name=todolist_name, name=task_name)

    def close_task(self, todolist_name: TodolistName, task_key: TaskKey):
        use_case: CloseTask = self.dependencies.get_use_case(CloseTask)
        use_case.execute(todolist_name=todolist_name, key=task_key)

    def reword_task(self, todolist_name: TodolistName, task_key: TaskKey, new_name: TaskName):
        use_case: RewordTask = self.dependencies.get_use_case(RewordTask)
        use_case.execute(todolist_name, task_key, new_name)

    def import_many_tasks_from_markdown(self, todolist_name: TodolistName, markdown: str):
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

    def postpone_task_to_tomorrow(self, name : TodolistName, key: TaskKey) -> None:
        tomorrow = self._datetime_provider.now() + timedelta(days=1)
        use_case: PostPoneTask = self.dependencies.get_use_case(PostPoneTask)
        use_case.execute(todolist_name=name, key=key, execution_date=TaskExecutionDate(tomorrow.date()))
