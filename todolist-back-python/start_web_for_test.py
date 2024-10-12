import os

from hexagon.todolist.aggregate import TodolistSetPort
from primary.controller.write.dependencies import inject_use_cases, Dependencies
from primary.web.pages import bottle_config, bottle_app
from test.hexagon.todolist.fixture import TodolistSetForTest

def inject_adapter(dependencies: Dependencies):
    todolist_set = TodolistSetForTest()
    dependencies = dependencies.feed_adapter(TodolistSetPort, lambda _: todolist_set)
    return dependencies

if __name__ == '__main__':
    from dotenv import load_dotenv
    dependencies = inject_use_cases(bottle_config.dependencies)
    dependencies = inject_adapter(dependencies=dependencies)
    bottle_config.dependencies = dependencies
    load_dotenv()

    host = os.environ["HOST"]
    port = os.environ["PORT"]
    bottle_app.run(reloader=True, host=host, port=port, debug=True)
