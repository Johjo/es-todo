from dataclasses import replace

from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from hexagon.shared.type import TaskName, TaskOpen, TodolistName
from primary.controller.read.todolist import Task
from primary.controller.read.todolist import TodolistSetReadPort as TodolistRead_Port_Todolist
from dependencies import Dependencies
from primary.web.pages import bottle_config
from test.hexagon.todolist.fixture import TodolistSetForTest, TaskKeyGeneratorForTest
from test.fixture import TodolistFaker
from test.primary.controller.read.test_query_one_task import TodolistForTest


def test_display_reword_task(todolist_set: TodolistSetForTest, task_key_generator: TaskKeyGeneratorForTest,
                             test_dependencies: Dependencies, app: TestApp, fake: TodolistFaker):
    todolist = TodolistForTest()
    dependencies = test_dependencies.feed_adapter(TodolistRead_Port_Todolist, lambda _: todolist)
    bottle_config.dependencies = dependencies

    reworded_task = replace(fake.a_task_old(1), name=TaskName("initial name"), is_open=TaskOpen(True))

    a_todolist = replace(fake.a_todolist_old(), name=TodolistName("todolist"), tasks=[reworded_task])
    todolist_set.feed(a_todolist)
    todolist.feed(a_todolist.name, reworded_task.key, Task(id=reworded_task.key, name=reworded_task.name, is_open=TaskOpen(True)))

    response = app.get(f'/todo/{a_todolist.name}/item/{reworded_task.key}/reword')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
