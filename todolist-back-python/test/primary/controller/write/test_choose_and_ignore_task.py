from typing import OrderedDict

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSnapshot
from hexagon.shared.type import TaskKey, UserKey
from infra.fvp_memory import FvpMemory
from primary.controller.write.todolist import TodolistWriteController
from test.fixture import a_task_key


def test_should_choose_and_ignore_when_one_task_already_chosen(fvp_memory: FvpMemory, dependencies: Dependencies):
    user_key = UserKey("the user")
    fvp_memory.feed(user_key=user_key, snapshot=FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1)})))

    sut = TodolistWriteController(dependencies)
    sut.choose_and_ignore_task(user_key=user_key, chosen_task=a_task_key(1), ignored_task=a_task_key(3))

    assert fvp_memory.by(user_key=user_key) == FvpSnapshot(
        OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1), a_task_key(3): a_task_key(1)}))
