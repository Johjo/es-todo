from domain.todo.todoapp import TodoApp
from hexagon.fvp.domain_model import Task
from hexagon.fvp.read.which_task import WhichTaskQuery, TaskReader
from toto import set_of_fvp_session_repository


class TaskReaderTodolist(TaskReader):
    def __init__(self, name):
        self.name = name

    def all(self) -> list[Task]:
        app = TodoApp()
        todolist_id = app.open_todolist(self.name)
        tasks = [Task(id=task.index, name=task.name) for task in app.get_open_items(todolist_id)]
        return tasks


def which_task(name):
    set_of_open_tasks = TaskReaderTodolist(name=name)
    response = WhichTaskQuery(set_of_open_tasks=set_of_open_tasks, set_of_fvp_sessions=set_of_fvp_session_repository).which_task()
    return response
