from dataclasses import replace

import pytest
from approvaltests import verify
from approvaltests.reporters import PythonNativeReporter
from expression import Option, Nothing, Some
from webtest import TestApp

from dependencies import Dependencies
from hexagon.shared.type import TodolistName, TodolistContext, TodolistContextCount, TaskKey
from hexagon.todolist.aggregate import TodolistSnapshot
from hexagon.todolist.port import TodolistSetPort
from primary.controller.read.todolist import TodolistSetReadPort, Task
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker, TodolistBuilder


class TodolistSetForTest(TodolistSetPort, TodolistSetReadPort):
    def task_by(self, todolist_name: str, task_key: TaskKey) -> Task:
        raise NotImplementedError()

    def all_by_name(self) -> list[TodolistName]:
        raise NotImplementedError()

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        return [(TodolistContext("#context_1"), TodolistContextCount(5)),
                (TodolistContext("#context_2"), TodolistContextCount(10)), ]

    def all_tasks(self, todolist_name: TodolistName) -> list[Task]:
        raise NotImplementedError()

    def __init__(self):
        self._todolist: dict[TodolistName, TodolistBuilder] = {}

    def by(self, todolist_name: TodolistName) -> Option[TodolistSnapshot]:
        if todolist_name not in self._todolist:
            return Nothing
        return Some(self._todolist[todolist_name].to_snapshot())

    def save_snapshot(self, snapshot: TodolistSnapshot) -> None:
        raise NotImplementedError()

    def feed(self, todolist: TodolistBuilder) -> None:
        self._todolist[todolist.name] = todolist


@pytest.fixture
def todolist_set() -> TodolistSetForTest:
    return TodolistSetForTest()


def test_show_when_no_task(todolist_set: TodolistSetForTest, test_dependencies: Dependencies, app: TestApp,
                           fake: TodolistFaker):
    test_dependencies = test_dependencies.feed_adapter(TodolistSetPort, lambda _: todolist_set)
    test_dependencies = test_dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set)
    bottle_config.dependencies = test_dependencies
    todolist_set.feed(fake.a_todolist(name="my_todolist"))

    response = app.get('/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())


def test_show_when_one_task(todolist_set: TodolistSetForTest, test_dependencies: Dependencies, app: TestApp,
                            fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    todolist_set.feed(fake.a_todolist(name="my_todolist").having(tasks=[fake.a_task(1).having(name="buy the milk")]))

    response = app.get('/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())


def test_show_when_two_tasks(todolist_set: TodolistSetForTest, test_dependencies: Dependencies, app: TestApp,
                             fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    todolist_set.feed(fake.a_todolist().having(
        name="my_todolist",
        tasks=[fake.a_task(1).having(name="buy the milk"), fake.a_task(2).having(name="buy the water")]))

    response = app.get('/todo/my_todolist')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
