from expression import Result

from src.dependencies import Dependencies
from src.hexagon.shared.type import TaskKey, TodolistKey
from src.hexagon.todolist.aggregate import TodolistAggregate
from src.hexagon.todolist.port import TodolistSetPort
from src.hexagon.todolist.write.update_todolist_aggregate import UpdateTodolistAggregate


class CloseTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_key: TodolistKey, task_key: TaskKey) -> Result[None, str]:
        def update(todolist: TodolistAggregate) -> Result[TodolistAggregate, str]:
            return todolist.close_task(task_key)

        return UpdateTodolistAggregate(self._todolist_set).execute(todolist_key, update)

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'CloseTask':
        return CloseTask(dependencies.get_adapter(TodolistSetPort))
