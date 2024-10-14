import os

from hexagon.fvp.port import FvpSessionSetPort
from hexagon.fvp.read.which_task import TodolistPort
from hexagon.todolist.aggregate import TodolistSetPort, TaskKey
from hexagon.todolist.write.open_task import TaskKeyGeneratorPort
from primary.controller.write.dependencies import inject_use_cases, Dependencies
from primary.web.pages import bottle_config, bottle_app
from secondary.fvp.simple_session_repository import FvpSessionSetForTest
from test.hexagon.todolist.fixture import TodolistSetForTest
from test.primary.web.conftest import TodolistForTest


class TaskKeyGeneratorIncremental(TaskKeyGeneratorPort):
    def __init__(self):
        self.current = 0

    def generate(self) -> TaskKey:
        self.current += 1
        return TaskKey(self.current)


def inject_adapter(dependencies: Dependencies):
    todolist_set = TodolistSetForTest()
    task_key_generator = TaskKeyGeneratorIncremental()
    todolist = TodolistForTest(todolist_set)
    fvp_session_set = FvpSessionSetForTest()
    dependencies = dependencies.feed_adapter(TodolistSetPort, lambda _: todolist_set)
    dependencies = dependencies.feed_adapter(TaskKeyGeneratorPort, lambda _: task_key_generator)
    dependencies = dependencies.feed_adapter(TodolistPort, lambda _: todolist)
    dependencies = dependencies.feed_adapter(FvpSessionSetPort, lambda _: fvp_session_set)
    return dependencies


def start():
    from dotenv import load_dotenv
    dependencies = inject_use_cases(bottle_config.dependencies)
    dependencies = inject_adapter(dependencies=dependencies)
    bottle_config.dependencies = dependencies
    load_dotenv()
    host = os.environ["HOST"]
    port = os.environ["PORT"]
    bottle_app.run(reloader=True, host=host, port=port, debug=True)


if __name__ == '__main__':
    start()
