from dataclasses import replace

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from hexagon.todolist.aggregate import TaskSnapshot
from dependencies import Dependencies
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TodolistFaker, TodolistSetForTest, TaskKeyGeneratorForTest
from test.primary.web.fixture import CleanResponse


def test_import_task(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest,
                     test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    expected_task = replace(fake.a_task(1), name="the imported task", is_open=True)

    todolist = replace(fake.a_todolist(), name="todolist")
    todolist_set.feed(todolist)
    task_key_generator.feed(expected_task.key)

    response = app.post(f'/todo/{todolist.name}/import', params={'markdown_import': markdown_from_tasks(expected_task)})
    assert response.status_code == 302
    assert CleanResponse(response).location() == f"/todo/{todolist.name}"
    assert expected_task in todolist_set.by(todolist.name).value.tasks


def markdown_from_tasks(*expected_tasks: TaskSnapshot) -> str:
    return "\n".join([f"- [ ] {task.name}" for task in expected_tasks])
