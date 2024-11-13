from dataclasses import replace

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from hexagon.shared.type import TaskOpen
from hexagon.todolist.aggregate import TaskSnapshot
from dependencies import Dependencies
from infra.memory import Memory
from primary.web.pages import bottle_config
from test.fixture import a_task_key, TodolistFaker
from test.hexagon.todolist.fixture import TodolistSetForTest, TaskKeyGeneratorForTest
from test.primary.web.fixture import CleanResponse


def test_close_task(memory: Memory, task_key_generator : TaskKeyGeneratorForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    expected_task = fake.a_task(1).having(is_open=TaskOpen(False))

    todolist = fake.a_todolist("todolist").having(tasks=[expected_task.having(is_open=TaskOpen(True))])
    memory.save(todolist.to_snapshot())

    response = app.post(f'/todo/{todolist.name}/item/{expected_task.key}/close')

    assert CleanResponse(response).location() == f"/todo/{todolist.name}"
    assert response.status_code == 302

    assert expected_task.to_snapshot() in memory.by(todolist.name).value.tasks

