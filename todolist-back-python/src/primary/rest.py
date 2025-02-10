from fastapi import FastAPI

from src.primary.todolist_routes import register_todolist_routes
from src.primary.use_cases_port import UseCasePort
from src.primary.user_routes import register_user_routes


def start_app(use_cases: UseCasePort):
    app = FastAPI()

    app = register_user_routes(app=app, use_cases=use_cases)
    app = register_todolist_routes(app=app, use_cases=use_cases)

    return app
