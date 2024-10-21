from approvaltests import verify
from approvaltests.reporters import PythonNativeReporter
from webtest import TestApp

from dependencies import Dependencies
from primary.controller.read.todolist import TodolistSetReadPort
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker
from test.primary.web.fixture import TodolistSetForTest


def test_display_export_as_markdown(todolist_set: TodolistSetForTest, test_dependencies: Dependencies, app: TestApp,
                                    fake: TodolistFaker):
    todolist_set = TodolistSetForTest()
    todolist = fake.a_todolist().having(name="todolist").having(tasks=[fake.a_task().having(name="buy milk"), fake.a_task().having(name="buy water")])
    todolist_set.feed(todolist)

    dependencies = test_dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set)
    bottle_config.dependencies = dependencies

    response = app.get(f'/todo/{todolist.name}/export')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
