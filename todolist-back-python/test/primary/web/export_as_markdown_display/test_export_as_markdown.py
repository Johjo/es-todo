from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from src.dependencies import Dependencies
from src.infra.memory import Memory
from src.primary.web.pages import bottle_config
from test.fixture import TodolistFaker
from test.primary.web.fixture import BASE_URL, header_with_good_authentication


def test_display_export_as_markdown(memory: Memory, dependencies: Dependencies, app: TestApp, fake: TodolistFaker) -> None:
    bottle_config.dependencies = dependencies

    todolist = fake.a_todolist().having(name="todolist").having(tasks=[fake.a_task().having(name="buy milk"), fake.a_task().having(name="buy water")])
    memory.save(user_key="test@mail.fr", todolist=todolist.to_snapshot())

    response = app.get(f'{BASE_URL}/{todolist.name}/export', headers=header_with_good_authentication())

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())


