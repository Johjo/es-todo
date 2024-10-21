from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from hexagon.shared.type import TaskName, TaskOpen
from primary.controller.read.todolist import Task
from primary.controller.read.todolist import TodolistSetReadPort as TodolistRead_Port_Todolist
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker
from test.primary.controller.read.test_query_one_task import TodolistForTest


def test_display_reword_task(app: TestApp, fake: TodolistFaker):
    todolist = TodolistForTest()
    dependencies = Dependencies.create_empty().feed_adapter(TodolistRead_Port_Todolist, lambda _: todolist)
    bottle_config.dependencies = dependencies

    reworded_task = fake.a_task(1).having(name=TaskName("initial name"), is_open=TaskOpen(True))

    a_todolist = fake.a_todolist(name="todolist").having(tasks=[reworded_task])

    todolist.feed(a_todolist.name, reworded_task.key,
                  Task(id=reworded_task.key, name=reworded_task.name, is_open=TaskOpen(True)))

    response = app.get(f'/todo/{a_todolist.name}/item/{reworded_task.key}/reword')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
