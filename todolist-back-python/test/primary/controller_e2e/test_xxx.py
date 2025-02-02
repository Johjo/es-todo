import sqlite3
from datetime import date
from uuid import UUID

import pytest
from dateutil.utils import today

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import ChooseTheTask, DoTheTask, NothingToDo
from src.hexagon.fvp.read.which_task import WhichTaskFilter
from src.hexagon.shared.type import TaskKey, TaskExecutionDate, TodolistName, TaskName, TaskOpen
from src.hexagon.todolist.port import TaskKeyGeneratorPort
from src.infra.sqlite.sdk import SqliteSdk
from src.primary.controller.read.final_version_perfected import FinalVersionPerfectedReadController
from src.primary.controller.read.todolist import TodolistReadController, TaskPresentation
from src.primary.controller.write.todolist import TodolistWriteController
from src.shared.const import USER_KEY
from src.primary.prod_dependencies import inject_all_dependencies


class TaskKeyGeneratorIncremental(TaskKeyGeneratorPort):
    def __init__(self) -> None:
        self.counter = 0

    def generate(self) -> TaskKey:
        self.counter += 1
        return TaskKey(UUID(int=self.counter))


@pytest.fixture
def task_key_generator() -> TaskKeyGeneratorPort:
    return TaskKeyGeneratorIncremental()


@pytest.fixture
def dependencies(task_key_generator: TaskKeyGeneratorPort) -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_path("sqlite_database_path", lambda _: ":memory:")
    dependencies = inject_all_dependencies(dependencies)
    dependencies = dependencies.feed_adapter(TaskKeyGeneratorPort, lambda _: task_key_generator)

    return dependencies


@pytest.fixture(autouse=True)
def create_table(dependencies: Dependencies):
    sdk = SqliteSdk(connection=dependencies.get_infrastructure(sqlite3.Connection))
    sdk.create_tables()


def test_xxx(dependencies: Dependencies) -> None:
    user_key = "the user"
    dependencies = dependencies.feed_data(USER_KEY, "user@mail.com")
    write = TodolistWriteController(dependencies)
    read = TodolistReadController(dependencies)
    fvp_read = FinalVersionPerfectedReadController(dependencies)
    todolist_name = TodolistName("todolist")
    which_task_filter = WhichTaskFilter(todolist_name=todolist_name, reference_date=date(2020, 10, 17))

    def which_task() -> NothingToDo | DoTheTask | ChooseTheTask:
        return fvp_read.which_task(user_key=user_key, todolist_name=todolist_name,
                                   include_context=which_task_filter.include_context,
                                   exclude_context=which_task_filter.exclude_context,
                                   task_filter=which_task_filter)


    write.create_todolist(todolist_name=todolist_name)
    assert read.all_todolist_by_name() == [todolist_name]

    write.open_task(todolist_name=todolist_name, task_name=TaskName("task 1 #context_1"))
    write.open_task(todolist_name=todolist_name, task_name=TaskName("task 2 #context_2"))

    assert read.counts_by_context(todolist_name=todolist_name) == [("#context_1", 1), ("#context_2", 1)]

    assert which_task() == ChooseTheTask(main_task_key=TaskKey(UUID(int=1)), secondary_task_key=TaskKey(UUID(int=2)))

    write.choose_and_ignore_task(user_key=user_key,chosen_task=TaskKey(UUID(int=1)), ignored_task=TaskKey(UUID(int=2)))

    assert which_task() == DoTheTask(key=TaskKey(UUID(int=1)))

    write.reset_all_priorities(user_key=user_key)
    assert which_task() == ChooseTheTask(main_task_key=TaskKey(UUID(int=1)), secondary_task_key=TaskKey(UUID(int=2)))

    write.postpone_task(name=todolist_name, key=TaskKey(UUID(int=1)), execution_date=TaskExecutionDate(today().date()))
    assert read.task_by(todolist_name=todolist_name,
                        task_key=TaskKey(UUID(int=1))) == TaskPresentation(
        key=TaskKey(UUID(int=1)),
        name=TaskName("task 1 #context_1"),
        is_open=TaskOpen(True), execution_date=TaskExecutionDate(today().date()))
