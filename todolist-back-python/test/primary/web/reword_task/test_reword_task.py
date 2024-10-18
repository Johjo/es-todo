from dataclasses import replace

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from hexagon.todolist.aggregate import TaskSnapshot
from dependencies import Dependencies
from primary.controller.write.todolist import TodolistWriteController
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TodolistFaker, a_task_key, TodolistSetForTest
from test.hexagon.todolist.write.test_open_task import TaskKeyGeneratorForTest


def test_reword_task(todolist_set: TodolistSetForTest, task_key_generator : TaskKeyGeneratorForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    initial_task = fake.a_task(1)
    expected_task = replace(initial_task, name="reworded")

    todolist = replace(fake.a_todolist(), name="todolist", tasks=[initial_task])
    todolist_set.feed(todolist)

    response = app.post(f'/todo/{todolist.name}/item/{expected_task.key.value}/reword', {"new_name": expected_task.name})

    assert response.status == '200 OK'
    assert expected_task in todolist_set.by(todolist.name).value.tasks
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())

