from dataclasses import dataclass

from domain.todo.todoapp import TodoApp
from domain.todo_markdown_exporter import TodoMarkdownExporter, TodoReader, Task as ExportedTask
from primary.controller.shared.count_open_items import count_open_items


def export_todo_list_to_markdown(name):
    view = ExportView(todolist_name=name,
                      markdown_export=TodoMarkdownExporter(TodoReaderApp(name)).export_to_markdown(),
                      number_of_items=count_open_items(name))
    return view


@dataclass
class ExportView:
    todolist_name: str
    number_of_items: int
    markdown_export: str


class TodoReaderApp(TodoReader):
    def __init__(self, name):
        self.app = TodoApp()
        self.name = name

    def all_tasks(self):
        self.app.open_todolist(self.name)
        todolist_id = self.app.open_todolist(self.name)
        return [ExportedTask(task.name, task.done) for task in self.app.all_tasks(todolist_id)]
