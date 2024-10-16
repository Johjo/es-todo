from primary.controller.read.todolist import TodolistReadController, TodolistSetReadPort, Task
from dependencies import Dependencies
from test.hexagon.todolist.fixture import TodolistFaker
from test.primary.controller.conftest import dependencies


class TodolistSetReadForTest(TodolistSetReadPort):
    def __init__(self) -> None:
        self._all_todolist: list[str] = []

    def all_by_name(self) -> list[str]:
        return self._all_todolist


    def task_by(self, todolist_name: str, task_key: int) -> Task:
        raise Exception("not implemented")

    def feed(self, *names: str):
        self._all_todolist = [n for n in names]


def test_query_all_todolist(dependencies: Dependencies, fake: TodolistFaker):
    todolist_set = TodolistSetReadForTest()
    first_todolist = fake.a_todolist()
    second_todolist = fake.a_todolist()

    todolist_set.feed(first_todolist.name, second_todolist.name)
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set)

    sut = TodolistReadController(dependencies)

    assert sut.all_todolist_by_name() == [first_todolist.name, second_todolist.name]
