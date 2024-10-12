from approvaltests import verify
from approvaltests.reporters import PythonNativeReporter
from webtest import TestApp

from primary.controller.write.dependencies import Dependencies
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TodolistFaker

def test_create_todolist(todolist_set, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies

    response = app.post('/todo', params={'name': "my_created_todolist"})

    print(response.body)
    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
