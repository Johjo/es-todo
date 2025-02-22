from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

from src.hexagon.shared.type import TodolistKey, TaskKey, TaskName, TodolistName
from src.hexagon.todolist.write.create_todolist import TodolistCreate
from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from src.primary.port import UseCaseDependenciesPort
from test.hexagon.todolist.write.test_delete_todolist import TodolistDelete


class OpenTask(BaseModel):
    name: str

class Todolist(BaseModel):
    name: str





def register_todolist_write_routes(app: FastAPI, use_cases: UseCaseDependenciesPort):
    @app.post("/todolist/{todolist_key}/task/{task_key}")
    async def open_task(todolist_key: UUID, task_key: UUID, task: OpenTask) -> None:
        use_case : OpenTaskUseCase = use_cases.open_task()
        use_case.execute(todolist_key=TodolistKey(todolist_key), task_key=TaskKey(task_key), name=TaskName(task.name))

    @app.post("/todolist/{todolist_key}")
    async def create_todolist(todolist_key: UUID, todolist: Todolist) -> None:
        use_case: TodolistCreate = use_cases.create_todolist()
        use_case.execute(todolist_key=TodolistKey(todolist_key), todolist_name=TodolistName(todolist.name))

    @app.delete("/todolist/{todolist_key}")
    async def delete_todolist(todolist_key: UUID) -> None:
        use_case: TodolistDelete = use_cases.delete_todolist()
        use_case.execute(todolist_key=TodolistKey(todolist_key))

    return app
