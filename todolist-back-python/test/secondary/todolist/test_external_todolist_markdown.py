import re

import pytest
from faker import Faker

from hexagon.todolist.write.import_many_task import ExternalTodoListPort, TaskImported
from test.fixture import TodolistFaker, TaskBuilder


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
    expected_task = imported_task_from(fake.a_task())

    markdown = markdown_from_tasks(expected_task)
    sut = MarkdownTodolist(markdown)

    assert sut.all_tasks() == [expected_task]


def test_read_many_task_from_markdown(fake: TodolistFaker):
    expected_tasks = [imported_task_from(fake.a_task()), imported_task_from(fake.a_task())]

    markdown = markdown_from_tasks(*expected_tasks)
    sut = MarkdownTodolist(markdown)

    assert sut.all_tasks() == expected_tasks


def test_read_closed_task(fake: TodolistFaker):
    expected_tasks = [imported_task_from(fake.a_closed_task())]

    markdown = markdown_from_tasks(*expected_tasks)
    sut = MarkdownTodolist(markdown)

    assert sut.all_tasks() == expected_tasks


@pytest.fixture
def fake() -> TodolistFaker:
    return TodolistFaker(Faker())


def markdown_from_tasks(*tasks: TaskImported) -> str:
    return "\n".join([f"- [{" " if task.is_open else "x"}] {task.name}" for task in tasks])


def imported_task_from(task: TaskBuilder) -> TaskImported:
    return TaskImported(name=task.to_name(), is_open=task.to_open())
