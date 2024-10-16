import pytest

from hexagon.todolist.port import TodolistSetPort
from primary.controller.dependencies import Dependencies
from primary.controller.write.todolist import TodolistWriteController
from test.hexagon.todolist.fixture import TodolistSetForTest


@pytest.mark.parametrize("todolist_name", ["my_todolist", "my_todolist2"])
def test_create_todolist(dependencies: Dependencies, todolist_name):
    todolist_set = TodolistSetForTest()
    dependencies = dependencies.feed_adapter(TodolistSetPort, lambda _: todolist_set)

    TodolistWriteController(dependencies).create_todolist(todolist_name)

    assert todolist_set.by(todolist_name).value.name == todolist_name
