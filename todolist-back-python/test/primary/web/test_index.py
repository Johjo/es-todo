from dataclasses import replace

import bottle  # type: ignore
from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter
from webtest import TestApp, TestResponse  # type: ignore

from primary.controller.dependencies import Dependencies
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TodolistFaker
from test.primary.web.conftest import app, fake


def test_index(todolist_set, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    todolist_set.feed(replace(fake.a_todolist(), name="1-todolist-1"))
    todolist_set.feed(replace(fake.a_todolist(), name="2-todolist-2"))

    response = app.get('/')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
