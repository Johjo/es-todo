from hexagon.todolist.port import TodolistSetPort
from primary.controller.read.todolist import TodolistReadController
from primary.controller.dependencies import Dependencies
from test.hexagon.todolist.fixture import TodolistSetForTest, TodolistFaker
from test.primary.controller.conftest import dependencies


def test_query_all_todolist(dependencies: Dependencies, fake: TodolistFaker):
    todolist_set = TodolistSetForTest()
    first_todolist = fake.a_todolist()
    second_todolist = fake.a_todolist()

    todolist_set.feed(first_todolist, second_todolist)
    dependencies = dependencies.feed_adapter(TodolistSetPort, lambda _: todolist_set)

    sut = TodolistReadController(dependencies)

    assert sut.all_todolist_by_name() == [first_todolist.name, second_todolist.name]
