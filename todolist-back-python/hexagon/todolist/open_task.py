from expression import Result, pipe

from hexagon.todolist.aggregate import TaskKey, TodolistAggregate, Task, TodolistSetPort


class OpenTask:
    def __init__(self, todolist_set: TodolistSetPort):
        self._todolist_set: TodolistSetPort = todolist_set

    def execute(self, key: TaskKey, name: str) -> Result[None, str]:
        return (
            self.load_aggregate()
            .map(lambda aggregate: aggregate.open_task(task=Task(key=key, name=name)))
            .map(self.save_aggregate)
        )

    def load_aggregate(self) -> Result[TodolistAggregate, str]:
        return self._todolist_set.by("my_todolist").map(TodolistAggregate.from_snapshot).to_result("todolist not found")

    def save_aggregate(self, aggregate: TodolistAggregate) -> None:
        return pipe(
            aggregate.to_snapshot(),
            self._todolist_set.save_snapshot
        )
