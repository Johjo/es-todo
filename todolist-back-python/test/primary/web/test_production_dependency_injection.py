import pytest

from dependencies import Dependencies
from start_web_for_test import inject_all_dependencies

@pytest.fixture
def sut() -> Dependencies:
    return inject_all_dependencies(Dependencies.create_empty())

def test_fvp_reset_session_use_case(sut: Dependencies):
    from hexagon.fvp.write.reset_fvp_session import ResetFvpSession
    assert isinstance(sut.get_use_case(ResetFvpSession), ResetFvpSession)

def test_fvp_cancel_priority_use_case(sut: Dependencies):
    from hexagon.fvp.write.cancel_priority import CancelPriority
    assert isinstance(sut.get_use_case(CancelPriority), CancelPriority)

def test_fvp_choose_and_ignore_task_use_case(sut: Dependencies):
    from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
    assert isinstance(sut.get_use_case(ChooseAndIgnoreTaskFvp), ChooseAndIgnoreTaskFvp)

def test_todolist_create_use_case(sut: Dependencies):
    from hexagon.todolist.write.create_todolist import TodolistCreate
    assert isinstance(sut.get_use_case(TodolistCreate), TodolistCreate)

def test_open_task_use_case(sut: Dependencies):
    from hexagon.todolist.write.open_task import OpenTaskUseCase
    assert isinstance(sut.get_use_case(OpenTaskUseCase), OpenTaskUseCase)

def test_close_task_use_case(sut: Dependencies):
    from hexagon.todolist.write.close_task import CloseTask
    assert isinstance(sut.get_use_case(CloseTask), CloseTask)

def test_reword_task_use_case(sut: Dependencies):
    from hexagon.todolist.write.reword_task import RewordTask
    assert isinstance(sut.get_use_case(RewordTask), RewordTask)

def test_import_many_task_use_case(sut: Dependencies):
    from hexagon.todolist.write.import_many_task import ImportManyTask
    assert isinstance(sut.get_use_case(ImportManyTask), ImportManyTask)

def test_which_task_query_use_case(sut: Dependencies):
    from hexagon.fvp.read.which_task import WhichTaskQuery
    assert isinstance(sut.get_use_case(WhichTaskQuery), WhichTaskQuery)
