from expression import Result

from hexagon.shared.type import TaskKey
from hexagon.todolist.port import TodolistSetPort
from hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


class CloseTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_name: str, key: TaskKey) -> Result[None, str]:
        update = lambda todolist: todolist.close_task(key)
        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_name, update)
