from expression import Result, pipe

from src.dependencies import Dependencies
from src.hexagon.shared.type import TodolistName, TaskKey, TaskExecutionDate
from src.hexagon.todolist.aggregate import TodolistAggregate
from src.hexagon.todolist.port import TodolistSetPort
from src.hexagon.todolist.todolist_repository import TodolistRepository


class PostPoneTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._repository = TodolistRepository(todolist_set)

    def execute(self, todolist_name: TodolistName, key: TaskKey, execution_date: TaskExecutionDate):
        def update(todolist: Result[TodolistAggregate, str]) -> Result[TodolistAggregate, str]:
            return todolist.bind(lambda t: t.postpone_task(key, execution_date))

        return pipe(todolist_name,
                    self._repository.load_todolist,
                    update,
                    self._repository.save_todolist)

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'PostPoneTask':
        todolist_set = dependencies.get_adapter(TodolistSetPort)
        return PostPoneTask(todolist_set)
