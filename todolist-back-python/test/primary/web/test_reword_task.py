from dataclasses import replace

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from primary.controller.read.todolist import TodolistRead, Task
from primary.controller.write.dependencies import Dependencies
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TodolistFaker, TodolistSetForTest
from test.hexagon.todolist.write.test_open_task import TaskKeyGeneratorForTest
from test.primary.controller.read.test_query_one_task import TodolistForTest


def test_display_reword_task(todolist_set: TodolistSetForTest, task_key_generator : TaskKeyGeneratorForTest, test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    todolist = TodolistForTest()
    dependencies = test_dependencies.feed_adapter(TodolistRead.Port.Todolist, lambda _: todolist)
    bottle_config.dependencies = dependencies

    reworded_task = replace(fake.a_task(1), name="initial name")

    a_todolist = replace(fake.a_todolist(), name="todolist", tasks=[reworded_task])
    todolist_set.feed(a_todolist)
    todolist.feed(a_todolist.name, 1, Task(id=1, name="initial name"))

    response = app.get(f'/todo/{a_todolist.name}/item/{1}/reword')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())

