from typing import OrderedDict

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSnapshot
from src.hexagon.shared.type import TaskKey
from src.infra.fvp_memory import FvpMemory
from src.primary.controller.write.todolist import TodolistWriteController
from test.fixture import a_task_key


def test_should_choose_and_ignore_when_one_task_already_chosen(fvp_memory: FvpMemory, dependencies: Dependencies):
    fvp_memory.feed(FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1)})))

    sut = TodolistWriteController(dependencies)
    sut.choose_and_ignore_task(chosen_task=a_task_key(1), ignored_task=a_task_key(3))

    assert fvp_memory.by() == FvpSnapshot(
        OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1), a_task_key(3): a_task_key(1)}))
