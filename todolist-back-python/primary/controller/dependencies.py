from functools import reduce

from dependencies import Dependencies, ResourceType
from hexagon.fvp.aggregate import FvpSessionSetPort
from hexagon.fvp.read.which_task import WhichTaskQuery, TodolistPort
from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from hexagon.todolist.port import TodolistSetPort, TaskKeyGeneratorPort
from hexagon.todolist.write.close_task import CloseTask
from hexagon.todolist.write.create_todolist import TodolistCreate
from hexagon.todolist.write.import_many_task import ImportManyTask
from hexagon.todolist.write.open_task import OpenTaskUseCase
from hexagon.todolist.write.reword_task import RewordTask


def inject_use_cases(dependencies: Dependencies) -> Dependencies:
    factories = {
        TodolistCreate: TodolistCreate.factory,
        OpenTaskUseCase: open_task_use_case_factory,
        CloseTask: close_task_use_case_factory,
        RewordTask: reword_task_use_case_factory,
        ImportManyTask: import_many_task_use_case_factory,
        WhichTaskQuery: which_task_query_factory,
        ChooseAndIgnoreTaskFvp: ChooseAndIgnoreTaskFvp.factory
    }

    def feed_use_case(dep: Dependencies, resource_and_factory) -> Dependencies:
        use_case, factory = resource_and_factory
        return dep.feed_use_case(use_case=use_case, use_case_factory=factory)

    return reduce(feed_use_case, factories.items(), dependencies)


def todolist_create_factory(dependencies: Dependencies):
    return TodolistCreate(dependencies.get_adapter(TodolistSetPort))


def open_task_use_case_factory(dependencies: Dependencies):
    todolist_set = dependencies.get_adapter(TodolistSetPort)
    task_key_generator = dependencies.get_adapter(TaskKeyGeneratorPort)
    return OpenTaskUseCase(todolist_set, task_key_generator)


def close_task_use_case_factory(dependencies):
    return CloseTask(dependencies.get_adapter(TodolistSetPort))


def reword_task_use_case_factory(dependencies: Dependencies) -> RewordTask:
    return RewordTask(dependencies.get_adapter(TodolistSetPort))


def import_many_task_use_case_factory(dependencies: Dependencies) -> ImportManyTask:
    return ImportManyTask(dependencies.get_adapter(TodolistSetPort))

def which_task_query_factory(dependencies: Dependencies) -> WhichTaskQuery:
    return WhichTaskQuery(dependencies.get_adapter(TodolistPort), dependencies.get_adapter(FvpSessionSetPort))
