from pathlib import Path

from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from primary.web.pages import bottle_config


def test_display_import(test_dependencies: Dependencies, app: TestApp) -> None:
    bottle_config.dependencies = test_dependencies.feed_path("static_path", lambda _: "../test/data_test/static")
    response = app.get(f'/static/test/file.txt')

    assert response.status == '200 OK'
    assert response.body == b"Should read this value in test"
