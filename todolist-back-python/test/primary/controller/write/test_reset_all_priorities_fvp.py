from typing import OrderedDict

import pytest
from faker.proxy import Faker

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSnapshot
from src.hexagon.shared.type import TaskKey, UserKey
from src.infra.fvp_memory import FvpMemory
from src.primary.controller.write.todolist import TodolistWriteController
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
