
from src.primary.controller.write.todolist import TodolistWriteController
from test.fixture import TodolistFaker
from test.primary.controller.write.conftest import TodolistSetForTest


def test_reword_task(todolist_set: TodolistSetForTest, sut: TodolistWriteController, fake: TodolistFaker):
    expected_task = fake.a_task()
    todolist = fake.a_todolist().having(tasks=[expected_task.having(name="buy the milk")])
    todolist_set.feed(todolist)

    sut.reword_task(todolist.to_name(), expected_task.to_key(), expected_task.to_name())

    actual = todolist_set.by(todolist.name).value
    assert actual == todolist.having(tasks=[expected_task]).to_snapshot()




