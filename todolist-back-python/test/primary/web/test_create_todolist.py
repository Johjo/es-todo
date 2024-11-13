from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from primary.web.pages import bottle_config
from test.primary.web.fixture import CleanResponse


def test_create_todolist(test_dependencies: Dependencies, app: TestApp):
    bottle_config.dependencies = test_dependencies

    response = app.post('/todo', params={'name': "my_created_todolist"})

    assert CleanResponse(response).location() == "/todo/my_created_todolist"
    assert response.status_code == 302
