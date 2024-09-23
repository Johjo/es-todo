from domain.todo.todoapp import TodoApp
from domain.todo_markdown_importer import TodoMarkdownImporter, TodoWriter


def import_todolist_from_markdown(name, markdown):
    TodoMarkdownImporter(TodoWriterApp(name)).import_from_markdown(markdown)

class TodoWriterApp(TodoWriter):
    def __init__(self, name):
        self.name = name

    def write(self, task):
        app = TodoApp()
        todolist_id = app.open_todolist(self.name)
        app.add_item(todolist_id, task.name)

