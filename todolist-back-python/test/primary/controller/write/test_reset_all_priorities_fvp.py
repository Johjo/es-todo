from typing import OrderedDict

import pytest
from faker.proxy import Faker

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSnapshot
from hexagon.shared.type import TaskKey, UserKey
from infra.fvp_memory import FvpMemory
from primary.controller.write.todolist import TodolistWriteController
from test.fixture import TodolistFaker


@pytest.fixture
def fake():
    return TodolistFaker(Faker())


def test_reset_all_priorities(fvp_memory: FvpMemory, fake: TodolistFaker, dependencies: Dependencies):
    user_key = UserKey("the user")
    fvp_memory.feed(user_key=user_key, snapshot=FvpSnapshot(OrderedDict[TaskKey, TaskKey](
        {fake.a_task(2).to_key(): fake.a_task(1).to_key(),
         fake.a_task(1).to_key(): fake.a_task(3).to_key()})))

    sut = TodolistWriteController(dependencies)
    sut.reset_all_priorities(user_key=user_key)

    assert fvp_memory.by(user_key=user_key) == FvpSnapshot(
        OrderedDict[TaskKey, TaskKey]())
