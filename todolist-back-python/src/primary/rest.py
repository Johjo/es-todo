from typing import Protocol
from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

from src.hexagon.shared.type import UserKey, TodolistKey, TodolistName
from src.hexagon.user.create_todolist import CreateTodolist


class UseCasePort(Protocol):
    def create_todolist(self) -> CreateTodolist:
        ...


class Todolist(BaseModel):
    name: str


def start_app(use_cases: UseCasePort):
    app = FastAPI()

    @app.post("/{user_key}/todolist/{todolist_key}")
    async def create_todolist_for_user(user_key: str, todolist_key: UUID, todolist: Todolist) -> None:
        create_todolist: CreateTodolist = use_cases.create_todolist()
        create_todolist.execute(user_key=UserKey(user_key), todolist_key = TodolistKey(todolist_key), todolist_name=TodolistName(todolist.name))

    return app
