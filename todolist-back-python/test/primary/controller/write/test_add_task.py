
from src.dependencies import Dependencies
from src.primary.controller.write.todolist import TodolistWriteController
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest
from test.primary.controller.write.conftest import TodolistSetForTest


def test_open_task_when_no_task(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest, sut: TodolistWriteController, dependencies: Dependencies, fake: TodolistFaker):
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)
    expected_task = fake.a_task()
    task_key_generator.feed(expected_task.to_key())

    sut.open_task(
        todolist_name=todolist.to_name(),
        task_name=expected_task.to_name())

    actual = todolist_set.by(todolist.name).value

    assert actual == todolist.having(tasks=[expected_task]).to_snapshot()
