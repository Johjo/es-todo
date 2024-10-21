from approvaltests import verify
from approvaltests.reporters import PythonNativeReporter
from webtest import TestApp

from dependencies import Dependencies
from hexagon.shared.type import TodolistName
from primary.controller.read.todolist import TodolistSetReadPort, Task
from primary.web.pages import bottle_config
from test.fixture import TodolistFaker, TodolistBuilder
from test.primary.controller.read.fixture import TodolistSetReadPortNotImplemented


class TodolistSetForTest(TodolistSetReadPortNotImplemented):
    def __init__(self) -> None:
        self.tasks_by_todolist: dict[TodolistName, list[Task]] = {}

    def feed(self, todolist: TodolistBuilder) -> None:
        self.tasks_by_todolist[todolist.name] = [task.to_task() for task in todolist.tasks]

    def all_tasks(self, todolist_name: TodolistName) -> list[Task]:
        if todolist_name not in self.tasks_by_todolist:
            raise Exception(f"feed todolist '{todolist_name}' before getting tasks")
        return self.tasks_by_todolist[todolist_name]



def test_display_export_as_markdown(todolist_set: TodolistSetForTest, test_dependencies: Dependencies, app: TestApp,
                                    fake: TodolistFaker):
    todolist_set = TodolistSetForTest()
    todolist = fake.a_todolist().having(name="todolist").having(tasks=[fake.a_task().having(name="buy milk"), fake.a_task().having(name="buy water")])
    todolist_set.feed(todolist)

    dependencies = test_dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set)
    bottle_config.dependencies = dependencies

    response = app.get(f'/todo/{todolist.name}/export')

    assert response.status == '200 OK'
    verify(str(response.body).replace("\\r\\n", "\r\n"), reporter=PythonNativeReporter())
