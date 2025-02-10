from fastapi import FastAPI

from src.primary.todolist.read.list_all_tasks import register_todolist_read_routes
from src.primary.todolist_write_routes import register_todolist_write_routes
from src.primary.port import UseCaseDependenciesPort, QueryDependenciesPort
from src.primary.user_routes import register_user_routes


def start_app(use_cases: UseCaseDependenciesPort, queries:QueryDependenciesPort):
    app = FastAPI()

    app = register_user_routes(app=app, use_cases=use_cases)
    app = register_todolist_write_routes(app=app, use_cases=use_cases)
    app = register_todolist_read_routes(app=app, queries=queries)

    return app
