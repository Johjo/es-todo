from dataclasses import replace

from hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from primary.controller.write.dependencies import Dependencies
from primary.controller.write.todolist import TodolistWriteController
from test.hexagon.todolist.fixture import TodolistSetForTest, TodolistFaker
from test.hexagon.todolist.write.test_open_task import TaskKeyGeneratorForTest


def test_open_task_when_no_task(dependencies: Dependencies, fake: TodolistFaker):
    todolist_set = TodolistSetForTest()
    todolist = fake.a_todolist()
    todolist_set.feed(todolist)
    expected_task = fake.a_task()
    task_key_generator = TaskKeyGeneratorForTest()
    task_key_generator.feed(expected_task.key)

    dependencies = dependencies.feed_adapter(TodolistSetPort, lambda _: todolist_set)
    dependencies = dependencies.feed_adapter(TaskKeyGeneratorPort, lambda _: task_key_generator)


    controller = TodolistWriteController(dependencies)
    controller.open_task(todolist_name=todolist.name,
                         task_name=expected_task.name)

    actual = todolist_set.by(todolist.name).value

    assert actual == replace(todolist, tasks=[expected_task])
