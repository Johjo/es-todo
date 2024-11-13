from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from infra.memory import Memory
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest
from test.primary.web.fixture import CleanResponse


def test_reword_task(memory: Memory, task_key_generator : TaskKeyGeneratorForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    # given
    bottle_config.dependencies = test_dependencies
    initial_task = fake.a_task()
    expected_task = initial_task.having(name="reworded")

    todolist = fake.a_todolist().having(tasks=[initial_task])
    memory.save(todolist.to_snapshot())

    # when
    response = app.post(f'/todo/{todolist.to_name()}/item/{expected_task.to_key()}/reword', {"new_name": expected_task.to_name()})

    # then
    assert expected_task.to_snapshot() in memory.by(todolist.to_name()).value.tasks
    assert CleanResponse(response).location() == f"/todo/{todolist.to_name()}"
    assert response.status_code == 302

