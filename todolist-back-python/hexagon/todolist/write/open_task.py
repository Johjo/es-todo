from expression import Result

from hexagon.todolist.aggregate import TaskKey, Task, TodolistSetPort
from hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


class OpenTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_name, key: TaskKey, name: str) -> Result[None, str]:
        update = lambda aggregate: aggregate.open_task(Task(key=key, name=name, is_open=True))
        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_name, update)
