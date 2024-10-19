import re
from dataclasses import replace

import pytest
from faker import Faker

from hexagon.todolist.aggregate import TaskSnapshot
from hexagon.todolist.write.import_many_task import ExternalTodoListPort, TaskImported
from test.hexagon.todolist.fixture import TodolistFaker


class MarkdownTodolist(ExternalTodoListPort):
    def __init__(self, markdown: str) -> None:
        self._markdown = markdown

    def all_tasks(self) -> list[TaskImported]:
        pattern = r"- \[([x ])\] (.+)"
        all_tasks = re.findall(pattern, self._markdown)
        return [TaskImported(name=task[1], is_open=task[0]!="x") for task in all_tasks]  # type: ignore


def test_read_no_task_from_markdown():
    sut = MarkdownTodolist("")
    assert sut.all_tasks() == []


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


def test_read_closed_task(fake: TodolistFaker):
    expected_tasks = [imported_task_from(replace(fake.a_task(1), is_open=False))]

    markdown = markdown_from_tasks(*expected_tasks)
    sut = MarkdownTodolist(markdown)

    assert sut.all_tasks() == expected_tasks


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def markdown_from_tasks(*tasks: TaskImported) -> str:
    return "\n".join([f"- [{" " if task.is_open else "x"}] {task.name}" for task in tasks])


def imported_task_from(task: TaskSnapshot) -> TaskImported:
    return TaskImported(name=task.name, is_open=task.is_open)
