from hexagon.shared.type import TaskKey, TodolistName, TodolistContext, TodolistContextCount
from primary.controller.read.todolist import TodolistReadController, TodolistSetReadPort, Task
from dependencies import Dependencies
from test.fixture import a_task_key
from test.hexagon.todolist.fixture import TodolistFaker


# todo move in a shared single file
class TodolistForTest(TodolistSetReadPort):
    def all_by_name(self):
        raise Exception("not implemented")

    def __init__(self) -> None:
        self._tasks: dict[(str, TaskKey,), Task] = {}

    def feed(self, todolist_name: str, task_key: TaskKey, task: Task):
        self._tasks[(todolist_name, task_key)] = task

    def task_by(self, todolist_name: str, task_key: int):
        assert self.already_fed(task_key, todolist_name), "task must be fed before being read"
        return self._tasks[(todolist_name, task_key)]

    def already_fed(self, task_key, todolist_name):
        return (todolist_name, task_key) in self._tasks

    def counts_by_context(self, todolist_name: TodolistName) -> list[tuple[TodolistContext, TodolistContextCount]]:
        raise NotImplementedError()


def test_query_one_task(dependencies: Dependencies, fake: TodolistFaker):
    todolist = TodolistForTest()
    dependencies = dependencies.feed_adapter(TodolistSetReadPort, lambda _: todolist)

    expected_task = Task(id=a_task_key(1), name="buy milk")
    todolist.feed(todolist_name="my todolist", task_key=a_task_key(1), task=expected_task)

    controller = TodolistReadController(dependencies)
    actual = controller.task_by("my todolist", expected_task.id)

    assert actual == expected_task
