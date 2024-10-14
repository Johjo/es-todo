import os

from hexagon.todolist.aggregate import TodolistSetPort, TaskKey
from hexagon.todolist.write.open_task import TaskKeyGeneratorPort
from primary.controller.write.dependencies import inject_use_cases, Dependencies
from primary.web.pages import bottle_config, bottle_app
from test.hexagon.todolist.fixture import TodolistSetForTest


class TaskKeyGeneratorIncremental(TaskKeyGeneratorPort):
    def __init__(self):
        self.current = 0

    def generate(self) -> TaskKey:
        self.current += 1
        return TaskKey(self.current)


def inject_adapter(dependencies: Dependencies):
    todolist_set = TodolistSetForTest()
    task_key_generator = TaskKeyGeneratorIncremental()
    dependencies = dependencies.feed_adapter(TodolistSetPort, lambda _: todolist_set)
    dependencies = dependencies.feed_adapter(TaskKeyGeneratorPort, lambda _: task_key_generator)
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
