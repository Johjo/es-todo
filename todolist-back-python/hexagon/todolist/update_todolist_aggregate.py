from expression import Result, pipe

from hexagon.todolist.aggregate import TodolistSetPort, TodolistAggregate


class UpdateTodolistAggregate:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set = todolist_set

    def execute(self, todolist_name, update) -> Result[None, str]:
        return self.load_aggregate(todolist_name).bind(update).map(self.save_aggregate)

    def load_aggregate(self, todolist_name) -> Result[TodolistAggregate, str]:
        return self._todolist_set.by(todolist_name).map(TodolistAggregate.from_snapshot).to_result("todolist not found")

    def save_aggregate(self, aggregate: TodolistAggregate) -> None:
        return pipe(
            aggregate.to_snapshot(),
            self._todolist_set.save_snapshot
        )
