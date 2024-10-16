from dataclasses import replace

from approvaltests import verify
from approvaltests.reporters import PythonNativeReporter
from webtest import TestApp

from hexagon.todolist.aggregate import TaskSnapshot
from primary.controller.dependencies import Dependencies
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TodolistFaker, a_task_key, TodolistSetForTest
from test.hexagon.todolist.write.test_open_task import TaskKeyGeneratorForTest


def test_open_task(todolist_set: TodolistSetForTest, task_key_generator : TaskKeyGeneratorForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    expected_task = TaskSnapshot(key=a_task_key(1), name="the task", is_open=True)

    todolist = replace(fake.a_todolist(), name="todolist")
    todolist_set.feed(todolist)
    task_key_generator.feed(expected_task.key)


    response = app.post(f'/todo/{todolist.name}/item', params={'task_name': expected_task.name})

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
    assert expected_task in todolist_set.by(todolist.name).value.tasks

