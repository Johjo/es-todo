import pytest

from src.primary.controller.write.todolist import TodolistWriteController
from test.primary.controller.write.conftest import TodolistSetForTest


@pytest.mark.parametrize("todolist_name", ["my_todolist", "my_todolist2"])
def test_create_todolist(todolist_set: TodolistSetForTest, sut: TodolistWriteController, todolist_name):
    todolist_set.feed_with_nothing(todolist_name)

    sut.create_todolist(todolist_name)

    assert todolist_set.by(todolist_name).value.name == todolist_name
