import pytest

from hexagon.todolist.aggregate import TodolistSetPort
from primary.controller.write.todolist import TodolistWriteController
from test.hexagon.todolist.fixture import TodolistSetForTest
from test.primary.controller.write.conftest import dependencies_with_use_cases


@pytest.mark.parametrize("todolist_name", ["my_todolist", "my_todolist2"])
def test_create_todolist(dependencies_with_use_cases, todolist_name):
    todolist_set = TodolistSetForTest()
    dependencies = dependencies_with_use_cases.feed_adapter(TodolistSetPort, lambda _: todolist_set)

    TodolistWriteController(dependencies).create_todolist(todolist_name)

    assert todolist_set.by(todolist_name).value.name == todolist_name
