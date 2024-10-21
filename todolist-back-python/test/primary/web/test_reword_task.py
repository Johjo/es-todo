from dataclasses import replace

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TodolistSetForTest, TaskKeyGeneratorForTest
from test.fixture import TodolistFaker
from test.primary.web.fixture import CleanResponse


def test_reword_task(todolist_set: TodolistSetForTest, task_key_generator : TaskKeyGeneratorForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    initial_task = fake.a_task_old(1)
    expected_task = replace(initial_task, name="reworded")

    todolist = replace(fake.a_todolist_old(), name="todolist", tasks=[initial_task])
    todolist_set.feed(todolist)

    response = app.post(f'/todo/{todolist.name}/item/{expected_task.key}/reword', {"new_name": expected_task.name})
    assert CleanResponse(response).location() == f"/todo/{todolist.name}"
    assert response.status_code == 302
    assert expected_task in todolist_set.by(todolist.name).value.tasks

