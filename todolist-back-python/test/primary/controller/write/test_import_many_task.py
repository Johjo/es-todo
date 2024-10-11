from dataclasses import replace

from hexagon.todolist.aggregate import TodolistSetPort
from primary.controller.write.dependencies import Dependencies
from primary.controller.write.todolist import TodolistWriteController
from test.hexagon.todolist.fixture import TodolistSetForTest, TodolistFaker


def test_import_many_task(dependencies: Dependencies, fake: TodolistFaker):
    expected_tasks = [fake.a_task(1), fake.a_task(2)]
    todolist = replace(fake.a_todolist(), tasks=[])
    todolist_set = TodolistSetForTest()
    todolist_set.feed(todolist)

    dependencies = dependencies.feed_adapter(TodolistSetPort, lambda _: todolist_set)
    controller = TodolistWriteController(dependencies)
    controller.import_many_tasks(expected_tasks, todolist.name)

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=expected_tasks)


