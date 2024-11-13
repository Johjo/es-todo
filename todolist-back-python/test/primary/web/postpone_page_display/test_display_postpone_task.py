from approvaltests import verify  # type: ignore
from approvaltests.reporters import PythonNativeReporter  # type: ignore
from webtest import TestApp  # type: ignore

from dependencies import Dependencies
from hexagon.shared.type import TaskName, TaskOpen
from primary.controller.read.todolist import TodolistSetReadPort as TodolistRead_Port_Todolist
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker
from test.primary.controller.read.test_query_one_task import TodolistForTest


def test_display_postpone_task(app: TestApp, fake: TodolistFaker):
    todolist = TodolistForTest()
    dependencies = Dependencies.create_empty().feed_adapter(TodolistRead_Port_Todolist, lambda _: todolist)
    bottle_config.dependencies = dependencies

    initial_task = fake.a_task(1).having(name=TaskName("initial name"), is_open=TaskOpen(True))
    reworded_task = initial_task.having(name=initial_task.name)

    a_todolist = fake.a_todolist(name="todolist").having(tasks=[initial_task])
    todolist.feed(a_todolist.name, initial_task.key, reworded_task.to_task())

    response = app.get(f'/todo/{a_todolist.name}/item/{initial_task.key}/postpone')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
