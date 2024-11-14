from dependencies import Dependencies
from hexagon.fvp.read.which_task import TaskFilter
from hexagon.shared.type import TodolistName
from primary.controller.read.todolist import TodolistSetReadPort, Task, TodolistReadController, to_markdown
from test.fixture import TodolistFaker, TodolistBuilder
from test.primary.controller.read.fixture import TodolistSetReadPortNotImplemented


def test_export_all_tasks_to_markdown_when_empty(dependencies: Dependencies, fake: TodolistFaker):
    todolist_set = TodolistSetReadForTest()
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)
    sut = TodolistReadController(dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set))
    assert sut.to_markdown(todolist.name) == ""


def test_export_all_tasks_to_markdown_when_one_task(dependencies: Dependencies, fake: TodolistFaker):
    todolist_set = TodolistSetReadForTest()

    todolist = fake.a_todolist().having(
        tasks=[fake.a_task().having(name="buy the milk"), fake.a_task().having(name="buy the water")])
    todolist_set.feed(todolist)

    sut = TodolistReadController(dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist_set))
    actual = sut.to_markdown(todolist.name)

    assert actual == to_markdown([task.to_task() for task in todolist.to_tasks()])


class TodolistSetReadForTest(TodolistSetReadPortNotImplemented):
    def __init__(self):
        self._tasks_by_todolist = dict[TodolistName, list[Task]]()

    def feed(self, todolist: TodolistBuilder):
        self._tasks_by_todolist[todolist.name] = [task.to_task() for task in todolist.to_tasks()]

    # todo task_filter
    def all_tasks(self, todolist_name: TodolistName, task_filter: TaskFilter) -> list[Task]:
        if todolist_name not in self._tasks_by_todolist:
            raise Exception(f"feed task for todolist '{todolist_name}' first")
        return self._tasks_by_todolist[todolist_name]
