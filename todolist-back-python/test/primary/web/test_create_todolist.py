from webtest import TestApp  # type: ignore

from src.dependencies import Dependencies
from src.primary.web.pages import bottle_config
from test.primary.web.fixture import CleanResponse, header_with_good_authentication


def test_create_todolist(test_dependencies: Dependencies, app: TestApp) -> None:
    bottle_config.dependencies = test_dependencies

    response = app.post('/todo', params={'name': "my_created_todolist"}, headers=header_with_good_authentication())

    assert CleanResponse(response).location() == "/todo/my_created_todolist"
    assert response.status_code == 302
