from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from infra.memory import Memory
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker
from test.primary.web.fixture import BASE_URL, header_with_good_authentication


def test_display_import(memory: Memory, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker) -> None:
    bottle_config.dependencies = test_dependencies

    todolist = fake.a_todolist("my_todolist")
    memory.save(user_key="test@mail.fr", todolist=todolist.to_snapshot())
    response = app.get(f'{BASE_URL}/{todolist.name}/import', headers=header_with_good_authentication())

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())

