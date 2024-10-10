from hexagon.todolist.aggregate import TodolistSetPort, TaskSnapshot
from hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


class ImportManyTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_name: str, tasks: list[TaskSnapshot]):
        update = lambda todolist: todolist.import_tasks(tasks)
        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_name, update)
