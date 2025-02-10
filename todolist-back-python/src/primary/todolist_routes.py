from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

from src.hexagon.shared.type import TodolistKey, TaskKey, TaskName
from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from src.primary.use_cases_port import UseCasePort

class OpenTask(BaseModel):
    name: str



def register_todolist_routes(app: FastAPI, use_cases: UseCasePort):

    @app.post("/todolist/{todolist_key}/{task_key}")
    async def open_task(todolist_key: UUID, task_key: UUID, task: OpenTask) -> None:
        use_case : OpenTaskUseCase = use_cases.open_task()
        use_case.execute(todolist_key=TodolistKey(todolist_key), task_key=TaskKey(task_key), name=TaskName(task.name))
    return app
