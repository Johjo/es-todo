import pytest

from domain.todo_markdown_exporter import TodoMarkdownExporter, TodoReader, Task


def test_export_empty_todo(sut):
    assert sut.export_to_markdown() == ""


@pytest.mark.parametrize("tasks, expected", [
    ([Task("Buy milk", done=False)], "- [ ] Buy milk"),
    ([Task("Buy milk", done=False), Task("Buy eggs", done=False)], "- [ ] Buy milk\n- [ ] Buy eggs"),
])
def test_export_open_task(sut, reader, tasks, expected):
    for task in tasks:
        reader.feed(task)
    assert sut.export_to_markdown() == expected


def test_export_closed_task(sut, reader):
    reader.feed(Task("Buy milk", done=True))
    assert sut.export_to_markdown() == "- [x] Buy milk"


@pytest.fixture
def reader():
    return SimpleTodoReader()


@pytest.fixture
def sut(reader):
    return TodoMarkdownExporter(reader)


class SimpleTodoReader(TodoReader):
    def __init__(self):
        self.tasks = []

    def feed(self, task):
        self.tasks.append(task)

    def all_tasks(self):
        return self.tasks
