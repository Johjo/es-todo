from expression import Result

from dependencies import Dependencies
from hexagon.shared.type import TaskKey
from hexagon.todolist.aggregate import TodolistAggregate
from hexagon.todolist.port import TodolistSetPort
from hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


class CloseTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_name: str, key: TaskKey) -> Result[None, str]:
        def update(todolist: TodolistAggregate) -> Result[TodolistAggregate, str]:
            return todolist.close_task(key)
        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_name, update)

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'CloseTask':
        return CloseTask(dependencies.get_adapter(TodolistSetPort))
