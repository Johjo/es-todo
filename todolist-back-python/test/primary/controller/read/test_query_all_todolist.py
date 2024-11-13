from hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount
from primary.controller.read.todolist import TodolistReadController, TodolistSetReadPort, Task
from dependencies import Dependencies
from test.fixture import TodolistFaker
from test.primary.controller.conftest import dependencies
from test.primary.controller.read.fixture import TodolistSetReadPortNotImplemented


class TodolistSetReadForTest(TodolistSetReadPortNotImplemented):
    def __init__(self) -> None:
        self._all_todolist: list[str] = []

    def feed(self, *names: str):
        self._all_todolist = [n for n in names]

    def all_by_name(self) -> list[str]:
        return self._all_todolist



def test_query_all_todolist(dependencies: Dependencies, fake: TodolistFaker):
    todolist_set = TodolistSetReadForTest()
    first_todolist = fake.a_todolist()
    second_todolist = fake.a_todolist()

    todolist_set.feed(first_todolist.to_name(), second_todolist.to_name())
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set)

    sut = TodolistReadController(dependencies)

    assert sut.all_todolist_by_name() == [first_todolist.to_name(), second_todolist.to_name()]
