from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from primary.web.pages import bottle_config
from test.primary.web.fixture import CleanResponse, header_with_good_authentication


def test_create_todolist(dependencies: Dependencies, app: TestApp) -> None:
    bottle_config.dependencies = dependencies

    response = app.post('/todo', params={'name': "my_created_todolist"}, headers=header_with_good_authentication())

    assert CleanResponse(response).location() == "/todo/my_created_todolist"
    assert response.status_code == 302
