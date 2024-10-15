import os

from hexagon.fvp.aggregate import FvpSessionSetPort, FinalVersionPerfected
from hexagon.fvp.read.which_task import TodolistPort
from hexagon.fvp.read.which_task import WhichTask
from hexagon.todolist.aggregate import TodolistSetPort, TaskKey, Todolist
from hexagon.todolist.write.open_task import TaskKeyGeneratorPort, OpenTask
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
    dependencies = dependencies.feed_adapter(Todolist.Port.TodolistSet, lambda _: todolist_set)

    task_key_generator = TaskKeyGeneratorIncremental()
    dependencies = dependencies.feed_adapter(OpenTask.Port.TaskKeyGenerator, lambda _: task_key_generator)

    which_task_todolist = TodolistForTest(todolist_set)
    dependencies = dependencies.feed_adapter(WhichTask.Port.Todolist, lambda _: which_task_todolist)

    fvp_session_set = FvpSessionSetForTest()
    dependencies = dependencies.feed_adapter(FinalVersionPerfected.Port.SessionSet, lambda _: fvp_session_set)

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
