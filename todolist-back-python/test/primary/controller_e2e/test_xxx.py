from uuid import UUID

import pytest
from dateutil.utils import today

from dependencies import Dependencies
from hexagon.fvp.aggregate import ChooseTheTask, DoTheTask
from hexagon.fvp.read.which_task import WhichTaskFilter
from hexagon.shared.type import TaskKey, TaskExecutionDate, TodolistName, TaskName, TaskOpen
from hexagon.todolist.port import TaskKeyGeneratorPort
from primary.controller.read.final_version_perfected import FinalVersionPerfectedReadController
from primary.controller.read.todolist import TodolistReadController, TaskPresentation, TaskFilter
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

    write.create_todolist(todolist_name=todolist_name)
    assert read.all_todolist_by_name() == [todolist_name]

    write.open_task(todolist_name=todolist_name, task_name=TaskName("task 1 #context_1"))
    write.open_task(todolist_name=todolist_name, task_name=TaskName("task 2 #context_2"))

    assert read.counts_by_context(todolist_name=todolist_name) == [("#context_1", 1), ("#context_2", 1)]
    assert fvp_read.which_task(WhichTaskFilter(todolist_name=todolist_name)) == ChooseTheTask(id_1=TaskKey(UUID(int=1)),
                                                                                            name_1="task 1 #context_1",
                                                                                            id_2=TaskKey(UUID(int=2)),
                                                                                            name_2="task 2 #context_2")

    write.choose_and_ignore_task(chosen_task=TaskKey(UUID(int=1)), ignored_task=TaskKey(UUID(int=2)))

    assert fvp_read.which_task(WhichTaskFilter(todolist_name=todolist_name)) == DoTheTask(id=TaskKey(UUID(int=1)), name="task 1 #context_1")

    write.reset_all_priorities()
    assert fvp_read.which_task(WhichTaskFilter(todolist_name=todolist_name)) == ChooseTheTask(id_1=TaskKey(UUID(int=1)),
                                                                                            name_1="task 1 #context_1",
                                                                                            id_2=TaskKey(UUID(int=2)),
                                                                                            name_2="task 2 #context_2")

    write.postpone_task(name=todolist_name, key=TaskKey(UUID(int=1)), execution_date=TaskExecutionDate(today().date()))
    assert read.task_by(todolist_name=todolist_name,
                        task_key=TaskKey(UUID(int=1))) == TaskPresentation(
        key=TaskKey(UUID(int=1)),
        name=TaskName("task 1 #context_1"),
        is_open=TaskOpen(True), execution_date=TaskExecutionDate(today().date()))
