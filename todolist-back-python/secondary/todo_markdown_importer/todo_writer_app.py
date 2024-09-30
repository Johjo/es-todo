from domain.todo.todoapp import TodoApp
from domain.todo_markdown_importer import TodoWriter


class TodoWriterApp(TodoWriter):
    def __init__(self, todolist_name):
        self.name = todolist_name

    def write(self, task):
        app = TodoApp()
        todolist_id = app.open_todolist(self.name)
        app.add_item(todolist_id, task.name)
