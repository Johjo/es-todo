
from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from infra.memory import Memory
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker
from test.primary.web.fixture import header_with_good_authentication


def test_index(memory: Memory, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker) -> None:
    bottle_config.dependencies = test_dependencies
    memory.save(user_key="test@mail.fr", todolist=fake.a_todolist("1-todolist-1").to_snapshot())
    memory.save(user_key="test@mail.fr", todolist=fake.a_todolist("2-todolist-2").to_snapshot())

    response = app.get('/todo', headers=header_with_good_authentication())

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
