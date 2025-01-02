from uuid import UUID

from expression import Option, Nothing, Some

from src.hexagon.todolist.aggregate import TodolistSnapshot, TaskSnapshot


class Memory:
    def __init__(self) -> None:
        self.all_todolist: dict[tuple[str, str], TodolistSnapshot] = {}

    def by(self, user_key: str, todolist_name: str) -> Option[TodolistSnapshot]:
        print(self.all_todolist)
        print(user_key, todolist_name)
        if (user_key, todolist_name) not in self.all_todolist:
            return Nothing
        return Some(self.all_todolist[(user_key, todolist_name)])

    def save(self, user_key: str, todolist: TodolistSnapshot):
        self.all_todolist[(user_key, todolist.name)] = todolist

    def task_by(self, user_key: str, todolist_name: str, task_key: UUID) -> TaskSnapshot:
        all_tasks = self.all_todolist[(user_key, todolist_name)].tasks
        task = [task for task in all_tasks if task.key == task_key][0]
        return task

    def all_todolist_by_name(self, user_key: str) -> list[str]:
        return [name for (todolist_user_key, name) in self.all_todolist.keys() if todolist_user_key == user_key]

    def all_tasks(self, user_key: str, todolist_name: str) -> list[TaskSnapshot]:
        if (user_key, todolist_name) not in self.all_todolist:
            return []
        return list(self.all_todolist[(user_key, todolist_name)].tasks)

    def __repr__(self):
        return str(self.all_todolist)


