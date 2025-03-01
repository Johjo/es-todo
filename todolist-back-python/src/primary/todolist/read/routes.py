from uuid import UUID

from fastapi import FastAPI

from src.hexagon.shared.type import TodolistKey
from src.primary.port import QueryDependenciesPort
from src.primary.todolist.read.port import AllTasksPresentation


def register_todolist_read_routes(app: FastAPI, queries: QueryDependenciesPort):
    @app.get("/todolist/{todolist_key}/task")
    async def list_all_tasks(todolist_key: UUID) -> AllTasksPresentation:
        query = queries.all_tasks()
        return query.all_tasks(todolist_key=TodolistKey(todolist_key))

    return app
