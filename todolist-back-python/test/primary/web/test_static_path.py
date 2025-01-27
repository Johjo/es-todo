
from webtest import TestApp  # type: ignore

from src.dependencies import Dependencies
from src.primary.web.pages import bottle_config


def test_display_import(dependencies: Dependencies, app: TestApp) -> None:
    bottle_config.dependencies = dependencies.feed_path("static_path", lambda _: "../test/data_test/static")
    response = app.get('/static/test/file.txt')

    assert response.status == '200 OK'
    assert response.body == b"Should read this value in test"
