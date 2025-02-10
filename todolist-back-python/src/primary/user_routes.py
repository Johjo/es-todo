from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

from src.hexagon.shared.type import UserKey, TodolistKey, TodolistName
from src.hexagon.user.create_todolist import CreateTodolist
from src.primary.port import UseCaseDependenciesPort


class Todolist(BaseModel):
    name: str

def register_user_routes(app: FastAPI, use_cases: UseCaseDependenciesPort):
    @app.post("/{user_key}/todolist/{todolist_key}")
    async def create_todolist_for_user(user_key: str, todolist_key: UUID, todolist: Todolist) -> None:
        create_todolist: CreateTodolist = use_cases.create_todolist()
        create_todolist.execute(user_key=UserKey(user_key), todolist_key=TodolistKey(todolist_key),
                                todolist_name=TodolistName(todolist.name))

    return app
