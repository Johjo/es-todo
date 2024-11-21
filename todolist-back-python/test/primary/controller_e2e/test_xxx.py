from datetime import date
from uuid import UUID

import pytest
from dateutil.utils import today

from dependencies import Dependencies
from hexagon.fvp.aggregate import ChooseTheTask, DoTheTask
from hexagon.fvp.read.which_task import WhichTaskFilter
from hexagon.shared.type import TaskKey, TaskExecutionDate, TodolistName, TaskName, TaskOpen
from hexagon.todolist.port import TaskKeyGeneratorPort
from primary.controller.read.final_version_perfected import FinalVersionPerfectedReadController
from primary.controller.read.todolist import TodolistReadController, TaskPresentation
from primary.controller.write.todolist import TodolistWriteController
from start_web_for_test import inject_all_dependencies


class TaskKeyGeneratorIncremental(TaskKeyGeneratorPort):
    def __init__(self):
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


def test_xxx(dependencies: Dependencies):
    write = TodolistWriteController(dependencies)
    read = TodolistReadController(dependencies)
    fvp_read = FinalVersionPerfectedReadController(dependencies)
    todolist_name = TodolistName("todolist")
    which_task_filter = WhichTaskFilter(todolist_name=todolist_name, reference_date=date(2020, 10, 17))

    def which_task():
        return fvp_read.which_task(todolist_name=todolist_name,
                                   include_context=which_task_filter.include_context,
                                   exclude_context=which_task_filter.exclude_context,
                                   task_filter=which_task_filter)


    write.create_todolist(todolist_name=todolist_name)
    assert read.all_todolist_by_name() == [todolist_name]

    write.open_task(todolist_name=todolist_name, task_name=TaskName("task 1 #context_1"))
    write.open_task(todolist_name=todolist_name, task_name=TaskName("task 2 #context_2"))

    assert read.counts_by_context(todolist_name=todolist_name) == [("#context_1", 1), ("#context_2", 1)]
    assert which_task() == ChooseTheTask(main_task_key=TaskKey(UUID(int=1)), secondary_task_key=TaskKey(UUID(int=2)))

    write.choose_and_ignore_task(chosen_task=TaskKey(UUID(int=1)), ignored_task=TaskKey(UUID(int=2)))

    assert which_task() == DoTheTask(key=TaskKey(UUID(int=1)))

    write.reset_all_priorities()
    assert which_task() == ChooseTheTask(main_task_key=TaskKey(UUID(int=1)), secondary_task_key=TaskKey(UUID(int=2)))

    write.postpone_task(name=todolist_name, key=TaskKey(UUID(int=1)), execution_date=TaskExecutionDate(today().date()))
    assert read.task_by(todolist_name=todolist_name,
                        task_key=TaskKey(UUID(int=1))) == TaskPresentation(
        key=TaskKey(UUID(int=1)),
        name=TaskName("task 1 #context_1"),
        is_open=TaskOpen(True), execution_date=TaskExecutionDate(today().date()))
