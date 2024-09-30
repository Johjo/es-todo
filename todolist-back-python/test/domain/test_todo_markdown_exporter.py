import pytest

from domain.todo_markdown_exporter import TodoMarkdownExporter, TodoReader, Task

class SimpleTodoReader(TodoReader):
    def __init__(self) -> None:
        self.tasks : list[Task] = []

    def feed(self, task: Task) -> None:
        self.tasks.append(task)

    def all_tasks(self) -> list[Task]:
        return self.tasks



def test_export_empty_todo(sut : TodoMarkdownExporter) -> None:
    assert sut.export_to_markdown() == ""


@pytest.mark.parametrize("tasks, expected", [
    ([Task("Buy milk", done=False)], "- [ ] Buy milk"),
    ([Task("Buy milk", done=False), Task("Buy eggs", done=False)], "- [ ] Buy milk\n- [ ] Buy eggs"),
])
def test_export_open_task(sut : TodoMarkdownExporter , reader : SimpleTodoReader, tasks : list[Task], expected : str) -> None:
    for task in tasks:
        reader.feed(task)
    assert sut.export_to_markdown() == expected


def test_export_closed_task(sut : TodoMarkdownExporter , reader : SimpleTodoReader) -> None:
    reader.feed(Task("Buy milk", done=True))
    assert sut.export_to_markdown() == "- [x] Buy milk"


@pytest.fixture
def reader() -> SimpleTodoReader:
    return SimpleTodoReader()


@pytest.fixture
def sut(reader: SimpleTodoReader) -> TodoMarkdownExporter:
    return TodoMarkdownExporter(reader)


