from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from hexagon.shared.type import TaskName
from infra.memory import Memory
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker


def test_display_postpone_task(app: TestApp, test_dependencies: Dependencies, memory: Memory, fake: TodolistFaker):
    # GIVEN
    bottle_config.dependencies = test_dependencies

    initial_task = fake.a_task(1).having(name=TaskName("initial name"))

    todolist = fake.a_todolist(name="todolist").having(tasks=[initial_task])
    memory.save(todolist.to_snapshot())

    # WHEN
    response = app.get(f'/todo/{todolist.name}/item/{initial_task.key}/postpone')

    # THEN
    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
