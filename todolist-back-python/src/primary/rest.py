from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.primary.port import UseCaseDependenciesPort, QueryDependenciesPort
from src.primary.todolist.read.list_all_tasks import register_todolist_read_routes
from src.primary.todolist_write_routes import register_todolist_write_routes
from src.primary.user_routes import register_user_routes


def start_app(use_cases: UseCaseDependenciesPort, queries:QueryDependenciesPort):
    app = FastAPI()

    app = register_user_routes(app=app, use_cases=use_cases)
    app = register_todolist_write_routes(app=app, use_cases=use_cases)
    app = register_todolist_read_routes(app=app, queries=queries)

    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:8000",
        "http://todolist-ytreza-dev.osc-fr1.scalingo.io"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
