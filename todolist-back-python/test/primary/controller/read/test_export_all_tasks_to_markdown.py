from dependencies import Dependencies
from hexagon.shared.type import TodolistName, TodolistContext, TodolistContextCount, TaskKey
from hexagon.todolist.aggregate import TaskSnapshot
from primary.controller.read.todolist import TodolistSetReadPort, Task, TodolistReadController, to_markdown
from test.fixture import TodolistFaker, TodolistBuilder
from test.primary.controller.read.fixture import TodolistSetReadPortNotImplemented


class TodolistSetReadForTest(TodolistSetReadPortNotImplemented):
    def __init__(self):
        self._tasks_by_todolist = dict[TodolistName, list[TaskSnapshot]]()

    def feed(self, todolist: TodolistBuilder):
        snapshot = todolist.to_snapshot()
        self._tasks_by_todolist[snapshot.name] = snapshot.tasks

    def all_tasks(self, todolist_name: TodolistName) -> list[TaskSnapshot]:
        if todolist_name not in self._tasks_by_todolist:
            raise Exception(f"feed task for todolist '{todolist_name}' first")
        return self._tasks_by_todolist[todolist_name]


def test_export_all_tasks_to_markdown_when_empty(dependencies: Dependencies, fake: TodolistFaker):
    sut = TodolistReadController(dependencies)

    assert sut.export_to_markdown() == ""


def test_export_all_tasks_to_markdown_when_one_task(dependencies: Dependencies, fake: TodolistFaker):
    todolist_set = TodolistSetReadForTest()

    todolist = fake.a_todolist().having(tasks=[fake.a_task().having(name="buy the milk"), fake.a_task().having(name="buy the water")])
    todolist_set.feed(todolist)

    dependencies = dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set)

    sut = TodolistReadController(dependencies)

    actual = sut.to_markdown(todolist.name)

    assert actual == to_markdown([task.to_task() for task in todolist.tasks])
