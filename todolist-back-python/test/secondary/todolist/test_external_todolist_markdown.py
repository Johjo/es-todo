import re
from dataclasses import replace, dataclass

import pytest
from faker import Faker

from hexagon.todolist.aggregate import TaskSnapshot
from hexagon.todolist.write.import_many_task import ExternalTodoListPort, TaskImported
from test.fixture import a_task_key
from test.hexagon.todolist.fixture import TodolistFaker
from test.hexagon.todolist.write.test_open_task import task_key_generator, TaskKeyGeneratorForTest


class MarkdownTodolist(ExternalTodoListPort):
    def __init__(self, markdown: str) -> None:
        self._markdown = markdown

    def all_tasks(self) -> list[TaskImported]:
        pattern = r"- \[ \] (.+)"

        all_tasks = re.findall(pattern, self._markdown)

        return [TaskImported(name=task_name, is_open=True) for task_name in all_tasks]  # type: ignore


def test_read_no_task_from_markdown():
    sut = MarkdownTodolist("")
    assert sut.all_tasks() == []




def imported_task_from(task: TaskSnapshot) -> TaskImported:
    return TaskImported(name=task.name, is_open=task.is_open)


def test_read_one_task_from_markdown(fake: TodolistFaker):
    expected_task = imported_task_from(fake.a_task(1))

    markdown = markdown_from_tasks(expected_task)
    sut = MarkdownTodolist(markdown)

    assert sut.all_tasks() == [expected_task]


def test_read_many_task_from_markdown(fake: TodolistFaker):
    expected_tasks = [imported_task_from(fake.a_task(1)), imported_task_from(fake.a_task(2))]

    markdown = markdown_from_tasks(*expected_tasks)
    sut = MarkdownTodolist(markdown)

    assert sut.all_tasks() == expected_tasks


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def markdown_from_tasks(*tasks: TaskImported) -> str:
    return "\n".join([f"- [ ] {task.name}" for task in tasks])

# def import_from_markdown(self, markdown):
#     # Expression régulière pour trouver les tâches au format '- [ ] Task'
#     pattern = r"- \[ \] (.+)"
#
#     # Rechercher toutes les correspondances dans le markdown
#     matches = re.findall(pattern, markdown)
#
#     # Pour chaque correspondance, créer une tâche
#     for task_description in matches:
#         self.writer.write(Task(task_description, done=False))
