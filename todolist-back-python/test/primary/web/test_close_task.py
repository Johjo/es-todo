from dataclasses import replace

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from hexagon.todolist.aggregate import TaskSnapshot
from dependencies import Dependencies
from primary.web.pages import bottle_config
from test.fixture import a_task_key
from test.hexagon.todolist.fixture import TodolistFaker, TodolistSetForTest, TaskKeyGeneratorForTest
from test.primary.web.fixture import CleanResponse


def test_close_task(todolist_set: TodolistSetForTest, task_key_generator : TaskKeyGeneratorForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    expected_task = TaskSnapshot(name="the task", is_open=False, key=a_task_key(1))

    todolist = replace(fake.a_todolist(), name="todolist", tasks=[replace(expected_task, is_open=True)])
    todolist_set.feed(todolist)

    response = app.post(f'/todo/{todolist.name}/item/{expected_task.key}/close')

    assert CleanResponse(response).location() == f"/todo/{todolist.name}"
    assert response.status_code == 302

    assert expected_task in todolist_set.by(todolist.name).value.tasks

