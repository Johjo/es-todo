from dataclasses import replace

from approvaltests import verify
from approvaltests.reporters import PythonNativeReporter
from webtest import TestApp

from primary.controller.write.dependencies import Dependencies
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TodolistFaker


def test_show_when_no_task(todolist_set, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    todolist_set.feed(replace(fake.a_todolist(), name="my_todolist"))

    response = app.get('/todo/my_todolist')

    print(response.body)
    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
