import os
from pathlib import Path

from dotenv import load_dotenv

from src.primary.prod_dependencies import inject_all_dependencies
from src.primary.web.pages import bottle_config, bottle_app


def start() -> None:
    load_dotenv()
    print(os.environ["HELLO"])
    host = os.environ["HOST"]
    port = os.environ["PORT"]
    database_path = os.environ["DATABASE_PATH"]
    dependencies = bottle_config.dependencies
    dependencies = dependencies.feed_path("sqlite_database_path", lambda _: Path(database_path))
    dependencies = inject_all_dependencies(dependencies)
    bottle_config.dependencies = dependencies
    bottle_app.run(reloader=True, host=host, port=port, debug=True)

if __name__ == '__main__':
    start()
