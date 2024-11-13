from uuid import UUID

from expression import Option, Nothing, Some

from hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot


class Memory:
    def __init__(self) -> None:
        self.all_todolist: dict[str, TodolistSnapshot] = {}

    def by(self, todolist_name: str) -> Option[TodolistSnapshot]:
        if todolist_name not in self.all_todolist:
            return Nothing
        return Some(self.all_todolist[todolist_name])

    def save(self, todolist: TodolistSnapshot):
        self.all_todolist[todolist.name] = todolist

    def task_by(self, todolist_name: str, task_key: UUID) -> TaskSnapshot:
        all_tasks = self.all_todolist[todolist_name].tasks
        task = [task for task in all_tasks if task.key == task_key][0]
        return task

    def all_todolist_by_name(self) -> list[str]:
        return [name for name in self.all_todolist.keys()]

    def all_tasks(self, todolist_name: str) -> list[TaskSnapshot]:
        if todolist_name not in self.all_todolist:
            return []
        return list(self.all_todolist[todolist_name].tasks)


