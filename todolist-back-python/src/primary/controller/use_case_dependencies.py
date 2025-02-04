from functools import reduce
from typing import Any

from src.dependencies import Dependencies
from src.hexagon.fvp.read.which_task import WhichTaskQuery
from src.hexagon.fvp.write.cancel_priority import CancelPriority
from src.hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from src.hexagon.fvp.write.reset_fvp_session import ResetFvpSession
from src.hexagon.todolist.write.close_task import CloseTask
from src.hexagon.todolist.write.create_todolist import TodolistCreate
from src.hexagon.todolist.write.import_many_task import ImportManyTask
from src.hexagon.todolist.write.open_task import OpenTaskUseCase
from src.hexagon.todolist.write.postpone_task import PostPoneTask
from src.hexagon.todolist.write.reword_task import RewordTask
from src.hexagon.user.create_todolist import CreateTodolist


def inject_use_cases(dependencies: Dependencies) -> Dependencies:
    use_cases_with_factory: list[Any] = [ResetFvpSession, CancelPriority, ChooseAndIgnoreTaskFvp, TodolistCreate,
                                         OpenTaskUseCase, CloseTask, RewordTask, ImportManyTask, WhichTaskQuery, PostPoneTask]

    def feed_use_case(dep: Dependencies, use_case: Any) -> Dependencies:
        return dep.feed_use_case(use_case=use_case, use_case_factory=use_case.factory)

    return reduce(feed_use_case, use_cases_with_factory, dependencies)
