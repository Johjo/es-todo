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


def test_open_task(memory: Memory, task_key_generator : TaskKeyGeneratorForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    expected_task = fake.a_task(1).having(name="the task", is_open=TaskOpen(True))

    todolist =  fake.a_todolist("todolist")
    memory.save(todolist.to_snapshot())
    task_key_generator.feed(expected_task.key)


    response = app.post(f'/todo/{todolist.name}/item', params={'task_name': expected_task.name})
    assert CleanResponse(response).location() == f"/todo/{todolist.name}"
    assert response.status_code == 302
    assert expected_task.to_snapshot() in memory.by(todolist.name).value.tasks

