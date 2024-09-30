from domain.todo.todoapp import TodoApp
from domain.todo_markdown_exporter import TodoReader, Task as ExportedTask


class TodoReaderApp(TodoReader):
    def __init__(self, name):
        self.app = TodoApp()
        self.name = name

    def all_tasks(self):
        self.app.open_todolist(self.name)
        todolist_id = self.app.open_todolist(self.name)
        return [ExportedTask(task.name, task.done) for task in self.app.all_tasks(todolist_id)]
