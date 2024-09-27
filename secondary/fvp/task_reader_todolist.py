from domain.todo.todoapp import TodoApp
from hexagon.fvp.domain_model import Task
from hexagon.fvp.read.which_task import TaskReader


class TaskReaderTodolist(TaskReader):
    def __init__(self, todolist_name):
        self.name = todolist_name

    def all(self) -> list[Task]:
        app = TodoApp()
        todolist_id = app.open_todolist(self.name)
        tasks = [Task(id=task.index, name=task.name) for task in app.get_open_items(todolist_id)]
        return tasks
