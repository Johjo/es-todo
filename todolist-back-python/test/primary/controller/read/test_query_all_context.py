from dependencies import Dependencies
from hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount
from primary.controller.read.todolist import TodolistSetReadPort, Task, TodolistReadController
from test.fixture import TodolistFaker
from test.primary.controller.read.fixture import TodolistSetReadPortNotImplemented


class TodolistSetReadForTest(TodolistSetReadPortNotImplemented):
    def __init__(self) -> None:
        self._all_contexts: dict[TodolistName, list[tuple[TodolistContext, TodolistContextCount]]] = {}

    def feed(self, todolist_name: TodolistName, *counts_by_context: tuple[str, int]):
        self._all_contexts[todolist_name] = [(TodolistContext(count[0]), TodolistContextCount(count[1])) for count in counts_by_context]

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        if not todolist_name in self._all_contexts:
            raise Exception(f"feed todolist {todolist_name} with context")
        return self._all_contexts[todolist_name]



def test_query_all_context(dependencies: Dependencies, fake: TodolistFaker):
    # given
    expected_count_by_contexts = [("#context1", 5), ("#context2", 10)]
    todolist_set = TodolistSetReadForTest()
    todolist = fake.a_todolist()
    todolist_set.feed(todolist.to_name(), expected_count_by_contexts[1], expected_count_by_contexts[0])
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set)

    # when
    sut = TodolistReadController(dependencies)

    # then
    assert sut.counts_by_context(todolist.to_name()) == expected_count_by_contexts
