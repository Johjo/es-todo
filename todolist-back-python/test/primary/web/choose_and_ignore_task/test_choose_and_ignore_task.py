from dataclasses import replace

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TodolistFaker, TodolistSetForTest
from test.hexagon.todolist.write.test_open_task import TaskKeyGeneratorForTest


def test_choose_and_ignore_task(todolist_set: TodolistSetForTest, task_key_generator : TaskKeyGeneratorForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    bottle_config.dependencies = test_dependencies
    task_1 = replace(fake.a_task(1), name="buy the milk")
    task_2 = replace(fake.a_task(2), name="buy the water")

    todolist = replace(fake.a_todolist(), name="todolist", tasks=[task_1, task_2])
    todolist_set.feed(todolist)


    response = app.post(f'/todo/{todolist.name}/item/choose/{task_1.key}/ignore/{task_2.key}')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
