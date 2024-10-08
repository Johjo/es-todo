import pytest
from expression import Ok, Error, Option, Some, Nothing, Result

from hexagon.todolist.create_todolist import TodolistSnapshot, TodolistCreate, TodolistSetPort


class TodolistSetForTest(TodolistSetPort):
    def __init__(self) -> None:
        self._all_snapshot: dict[str, TodolistSnapshot] = {}

    def save(self, todolist: TodolistSnapshot) -> None:
        self._all_snapshot[todolist.name] = todolist

    def history(self):
        return [name for name in self._all_snapshot]

    def feed(self, snapshot: TodolistSnapshot):
        self._all_snapshot[snapshot.name] = snapshot

    def by(self, todolist_name: str) -> Option[TodolistSnapshot]:
        if todolist_name not in self._all_snapshot:
            return Nothing
        return Some(self._all_snapshot[todolist_name])


@pytest.mark.parametrize("expected", [
    "my_todolist",
    "other_todolist",
])
def test_create_todolist(expected) -> None:
    todolist_set = TodolistSetForTest()

    response = TodolistCreate(todolist_set).execute(todolist_name=expected)

    assert todolist_set.by(expected) == Some(TodolistSnapshot(expected))
    assert response == Ok(None)


def test_tell_error_when_create_existing_todolist() -> None:
    todolist_set = TodolistSetForTest()
    todolist_set.feed(TodolistSnapshot("my_todolist"))

    response: Result[None, None] = TodolistCreate(todolist_set).execute(todolist_name="my_todolist")

    assert response == Error(None)
