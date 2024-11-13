from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from infra.memory import Memory
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker


def test_display_export_as_markdown(memory: Memory, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies

    todolist = fake.a_todolist().having(name="todolist").having(tasks=[fake.a_task().having(name="buy milk"), fake.a_task().having(name="buy water")])
    memory.save(todolist.to_snapshot())

    response = app.get(f'/todo/{todolist.name}/export')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
