from dataclasses import replace

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from primary.controller.read.todolist import TodolistSetReadPort
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker
from test.primary.web.todolist_display_page.test_show_todolist import TodolistSetForTest


def test_display_import(todolist_set: TodolistSetForTest, test_dependencies: Dependencies, app: TestApp,
                           fake: TodolistFaker):
    todolist_set = TodolistSetForTest()
    dependencies = test_dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set)


    bottle_config.dependencies = dependencies
    todolist = fake.a_todolist("my_todolist")
    todolist_set.feed(todolist)

    response = app.get(f'/todo/{todolist.name}/import')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())

