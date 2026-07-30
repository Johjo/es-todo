from typing import OrderedDict

import pytest

from dependencies import Dependencies
from hexagon.shared.type import TaskKey, UserKey
from infra.fvp_memory import FvpMemory
from primary.controller.write.todolist import TodolistWriteController
from secondary.fvp.write.fvp_session_set_in_memory import FvpSessionSetInMemory
from test.fixture import a_task_key
from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp


@pytest.fixture
def set_of_fvp_sessions(dependencies: Dependencies) -> FvpSessionSetInMemory:
    return dependencies.get_adapter(FvpSessionSetPort)


@pytest.fixture
def sut(set_of_fvp_sessions):
    return ChooseAndIgnoreTaskFvp(set_of_fvp_sessions)


def test_should_choose_and_ignore_when_one_task_already_chosen(fvp_memory: FvpMemory, dependencies: Dependencies):
    user_key = UserKey("the user")
    fvp_memory.feed(user_key=user_key, snapshot=FvpSnapshot(OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1), a_task_key(1): a_task_key(3)})))

    sut = TodolistWriteController(dependencies)
    sut.cancel_priority(user_key=user_key, task_key=a_task_key(3))

    assert fvp_memory.by(user_key=user_key) == FvpSnapshot(
        OrderedDict[TaskKey, TaskKey]({a_task_key(2): a_task_key(1)}))
