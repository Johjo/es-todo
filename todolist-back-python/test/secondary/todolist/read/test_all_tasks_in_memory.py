from uuid import uuid4

import pytest
from faker import Faker

from src.infra.memory import Memory
from src.primary.todolist.read.port import AllTasksPresentation, TaskPresentation
from src.secondary.todolist.read.all_tasks.all_tasks_in_memory import AllTaskInMemory
from test.fixture import TodolistFaker


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def test_xxx(fake: TodolistFaker):
    # GIVEN
    memory = Memory()
    sut = AllTaskInMemory(memory=memory)
    task_one = fake.a_task().having(execution_date=fake.a_date(), is_open=False)
    task_two = fake.a_task().having(is_open=True)

    todolist = fake.a_todolist().having(tasks=[task_one, task_two])
    memory.save(user_key=f"any_user{uuid4()}", todolist=todolist.to_snapshot())

    # WHEN
    actual = sut.all_tasks(todolist_key=todolist.to_key())

    # THEN
    assert actual == AllTasksPresentation(tasks=[
        TaskPresentation(key=task_one.to_key(), name=task_one.to_name(), open=False,
                         execution_date=task_one.to_execution_date().value),
        TaskPresentation(key=task_two.to_key(), name=task_two.to_name(), open=True, execution_date=None),
    ])
