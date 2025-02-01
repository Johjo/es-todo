from src.dependencies import Dependencies
from src.hexagon.shared.type import UserKey, TodolistName
from src.hexagon.user.create_todolist import CreateTodolist


class UserController:
    def __init__(self, dependencies: Dependencies):
        self._dependencies = dependencies

    def create_todolist(self, user_key: str, todolist_name: str):
        use_case: CreateTodolist = self._dependencies.get_use_case(CreateTodolist)
        use_case.execute(user_key=UserKey(user_key), todolist_name=TodolistName(todolist_name))
