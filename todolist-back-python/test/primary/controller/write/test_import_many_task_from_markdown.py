from dataclasses import replace

from hexagon.todolist.aggregate import TaskSnapshot
from primary.controller.write.todolist import TodolistWriteController
from test.hexagon.todolist.fixture import TaskKeyGeneratorForTest
from test.fixture import TodolistFaker
from test.primary.controller.write.conftest import TodolistSetForTest


def test_import_many_task_from_markdown(todolist_set: TodolistSetForTest, sut: TodolistWriteController, task_key_generator: TaskKeyGeneratorForTest, fake: TodolistFaker):
    expected_tasks = [fake.a_task_old(1), fake.a_task_old(2)]
    markdown = markdown_from_tasks(expected_tasks)

    todolist = replace(fake.a_todolist_old(), tasks=[])
    todolist_set.feed(todolist)
    task_key_generator.feed(*[task.key for task in expected_tasks])

    sut.import_many_tasks_from_markdown(todolist.name, markdown)

    actual = todolist_set.by(todolist.name).value
    assert actual == replace(todolist, tasks=expected_tasks)


def markdown_from_tasks(expected_tasks: list[TaskSnapshot]) -> str:
    return "\n".join([f"- [ ] {task.name}" for task in expected_tasks])


