from dataclasses import replace

from approvaltests import verify
from approvaltests.reporters import PythonNativeReporter
from webtest import TestApp

from dependencies import Dependencies
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TodolistSetForTest
from test.fixture import TodolistFaker


def test_display_import(todolist_set: TodolistSetForTest, test_dependencies: Dependencies, app: TestApp,
                           fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    todolist = replace(fake.a_todolist_old(), name="my_todolist")
    todolist_set.feed(todolist)

    response = app.get(f'/todo/{todolist.name}/import')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())

