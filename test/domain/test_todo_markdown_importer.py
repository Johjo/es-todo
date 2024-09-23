import pytest

from domain.todo_markdown_importer import TodoMarkdownImporter, TodoWriter, Task


class SimpleTodoWriter(TodoWriter):
    def __init__(self):
        self.tasks = []

    def write(self, task):
        self.tasks.append(task)


@pytest.fixture
def writer():
    return SimpleTodoWriter()

@pytest.fixture
def sut(writer):
    return TodoMarkdownImporter(writer)

def test_import_empty_todo(sut, writer):
    sut.import_from_markdown("")

    assert writer.tasks == []




@pytest.mark.parametrize("markdown, expected", [
    ("- [ ] Buy milk", [Task("Buy milk")]),
    ("- [ ] Buy water", [Task("Buy water")]),
    ("- [ ] Buy water\n- [ ] Buy milk", [Task("Buy water"), Task("Buy milk")]),
])
def test_import_tasks(sut, writer, markdown, expected):
    sut.import_from_markdown(markdown)
    assert writer.tasks == expected






