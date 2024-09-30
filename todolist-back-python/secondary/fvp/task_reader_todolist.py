from domain.todo.todoapp import TodoApp
from hexagon.fvp.domain_model import Task
from hexagon.fvp.read.which_task import TaskReader


# todo: cette classe est difficile à tester parce qu'elle utilise todoapp
class TaskReaderTodolist(TaskReader):
    def __init__(self, todolist_name: str, only_inbox: bool, context: str):
        self.name = todolist_name
        self.only_inbox = only_inbox
        self.context = context

    def all(self) -> list[Task]:
        app = TodoApp()
        todolist_id = app.open_todolist(self.name)
        tasks = [Task(id=task.index, name=task.name) for task in app.get_open_items(todolist_id)]

        if self.only_inbox:
            tasks = [task for task in tasks if "#" not in task.name]

        if self.context:
            tasks = [task for task in tasks if self.context in task.name]

        return tasks
