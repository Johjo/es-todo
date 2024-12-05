from expression import Result, pipe

from dependencies import Dependencies
from hexagon.shared.type import TodolistName, TaskKey, TaskExecutionDate
from hexagon.todolist.aggregate import TodolistAggregate
from hexagon.todolist.port import TodolistSetPort
from hexagon.todolist.todolist_repository import TodolistRepository


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

    @staticmethod
    def factory(dependencies: Dependencies) -> 'PostPoneTask':
        todolist_set = dependencies.get_adapter(TodolistSetPort)
        return PostPoneTask(todolist_set)
