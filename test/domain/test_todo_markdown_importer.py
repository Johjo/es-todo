import pytest

from domain.todo_markdown_importer import TodoMarkdownImporter, TodoWriter, Task


class SimpleTodoWriter(TodoWriter):
    def __init__(self) -> None:
        self.tasks : list[Task] = []

    def write(self, task : Task) -> None:
        self.tasks.append(task)


@pytest.fixture
def writer() -> SimpleTodoWriter:
    return SimpleTodoWriter()


@pytest.fixture
def sut(writer : SimpleTodoWriter) -> TodoMarkdownImporter:
    return TodoMarkdownImporter(writer)


def test_import_empty_todo(sut : TodoMarkdownImporter, writer: SimpleTodoWriter) -> None:
    sut.import_from_markdown("")
    assert writer.tasks == []


@pytest.mark.parametrize("markdown, expected", [
    ("- [ ] Buy milk", [Task("Buy milk")]),
    ("- [ ] Buy water", [Task("Buy water")]),
    ("- [ ] Buy water\n- [ ] Buy milk", [Task("Buy water"), Task("Buy milk")]),
])
def test_import_tasks(sut: TodoMarkdownImporter, writer: SimpleTodoWriter, markdown: str, expected: list[Task]) -> None:
    sut.import_from_markdown(markdown)
    assert writer.tasks == expected
