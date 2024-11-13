from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from infra.memory import Memory
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker, TaskBuilder
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest
from test.primary.web.fixture import CleanResponse


def test_import_task(memory: Memory, task_key_generator: TaskKeyGeneratorForTest,
                     test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    # given
    bottle_config.dependencies = test_dependencies
    expected_task = fake.a_task()

    todolist = fake.a_todolist()
    memory.save(todolist.to_snapshot())
    task_key_generator.feed(expected_task.to_key())

    # when
    response = app.post(f'/todo/{todolist.to_name()}/import', params={'markdown_import': markdown_from_tasks(expected_task)})

    # then
    assert response.status_code == 302
    assert CleanResponse(response).location() == f"/todo/{todolist.to_name()}"
    assert expected_task.to_snapshot() in memory.by(todolist.to_name()).value.tasks


def markdown_from_tasks(*expected_tasks: TaskBuilder) -> str:
    return "\n".join([f"- [ ] {task.to_name()}" for task in expected_tasks])
