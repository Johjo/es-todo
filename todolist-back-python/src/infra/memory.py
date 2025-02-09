from uuid import UUID

from expression import Option, Nothing, Some

from src.hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot


class Memory:
    def __init__(self) -> None:
        self.all_todolist: dict[tuple[str, UUID], TodolistSnapshot] = {}

    def by(self, user_key: str, todolist_key: UUID) -> Option[TodolistSnapshot]:
        if (user_key, todolist_key) not in self.all_todolist:
            return Nothing
        return Some(self.all_todolist[(user_key, todolist_key)])

    def save(self, user_key: str, todolist: TodolistSnapshot):
        self.all_todolist[(user_key, todolist.key)] = todolist

    def task_by(self, user_key: str, todolist_key: UUID, task_key: UUID) -> TaskSnapshot:
        all_tasks = self.all_todolist[(user_key, todolist_key)].tasks
        task = [task for task in all_tasks if task.key == task_key][0]
        return task

    def all_todolist_by_name(self, user_key: str) -> list[str]:
        return [self.all_todolist[(todolist_user_key, todolist_key)].name for (todolist_user_key, todolist_key) in self.all_todolist.keys() if todolist_user_key == user_key]

    def all_tasks(self, user_key: str, todolist_key: UUID) -> list[TaskSnapshot]:
        if (user_key, todolist_key) not in self.all_todolist:
            return []
        return list(self.all_todolist[(user_key, todolist_key)].tasks)

    def __repr__(self):
        return str(self.all_todolist)


