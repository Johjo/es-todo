from functools import reduce
from typing import Any

from dependencies import Dependencies
from hexagon.fvp.read.which_task import WhichTaskQuery
from hexagon.fvp.write.cancel_priority import CancelPriority
from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from hexagon.fvp.write.reset_fvp_session import ResetFvpSession
from hexagon.todolist.write.close_task import CloseTask
from hexagon.todolist.write.create_todolist import TodolistCreate
from hexagon.todolist.write.import_many_task import ImportManyTask
from hexagon.todolist.write.open_task import OpenTaskUseCase
from hexagon.todolist.write.reword_task import RewordTask


def inject_use_cases(dependencies: Dependencies) -> Dependencies:
    use_cases_with_factory: list[Any] = [ResetFvpSession, CancelPriority, ChooseAndIgnoreTaskFvp, TodolistCreate,
                                         OpenTaskUseCase, CloseTask, RewordTask, ImportManyTask, WhichTaskQuery]

    def feed_use_case(dep: Dependencies, use_case: Any) -> Dependencies:
        return dep.feed_use_case(use_case=use_case, use_case_factory=use_case.factory)

    return reduce(feed_use_case, use_cases_with_factory, dependencies)


