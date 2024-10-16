from approvaltests import verify
from approvaltests.reporters import PythonNativeReporter
from webtest import TestApp

from primary.controller.dependencies import Dependencies
from primary.web.pages import bottle_config


def test_create_todolist(test_dependencies: Dependencies, app: TestApp):
    bottle_config.dependencies = test_dependencies

    response = app.post('/todo', params={'name': "my_created_todolist"})

    print(response.body)
    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
