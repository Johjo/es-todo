import pytest

from src.dependencies import Dependencies
from src.primary.controller.write.todolist import TodolistWriteController
from src.shared.const import USER_KEY
from start_web_for_test import inject_all_dependencies

@pytest.fixture
def sut() -> Dependencies:
    dependencies = Dependencies.create_empty()
    dependencies = dependencies.feed_path("sqlite_database_path", lambda _: ":memory:")
    dependencies = dependencies.feed_data(data_name=USER_KEY, value="any value")
    dependencies = inject_all_dependencies(dependencies)
    return dependencies

def test_fvp_reset_session_use_case(sut: Dependencies) -> None:
    from src.hexagon.fvp.write.reset_fvp_session import ResetFvpSession
    assert isinstance(sut.get_use_case(ResetFvpSession), ResetFvpSession)

def test_fvp_cancel_priority_use_case(sut: Dependencies) -> None:
    from src.hexagon.fvp.write.cancel_priority import CancelPriority
    assert isinstance(sut.get_use_case(CancelPriority), CancelPriority)

def test_fvp_choose_and_ignore_task_use_case(sut: Dependencies) -> None:
    from src.hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
    assert isinstance(sut.get_use_case(ChooseAndIgnoreTaskFvp), ChooseAndIgnoreTaskFvp)

def test_todolist_create_use_case(sut: Dependencies) -> None:
    from src.hexagon.todolist.write.create_todolist import TodolistCreate
    assert isinstance(sut.get_use_case(TodolistCreate), TodolistCreate)

def test_open_task_use_case(sut: Dependencies) -> None:
    from src.hexagon.todolist.write.open_task import OpenTaskUseCase
    assert isinstance(sut.get_use_case(OpenTaskUseCase), OpenTaskUseCase)

def test_close_task_use_case(sut: Dependencies) -> None:
    from src.hexagon.todolist.write.close_task import CloseTask
    assert isinstance(sut.get_use_case(CloseTask), CloseTask)

def test_reword_task_use_case(sut: Dependencies) -> None:
    from src.hexagon.todolist.write.reword_task import RewordTask
    assert isinstance(sut.get_use_case(RewordTask), RewordTask)

def test_import_many_task_use_case(sut: Dependencies) -> None:
    from src.hexagon.todolist.write.import_many_task import ImportManyTask
    assert isinstance(sut.get_use_case(ImportManyTask), ImportManyTask)

def test_which_task_query_use_case(sut: Dependencies) -> None:
    from src.hexagon.fvp.read.which_task import WhichTaskQuery
    assert isinstance(sut.get_use_case(WhichTaskQuery), WhichTaskQuery)

def test_write_controller(sut: Dependencies) -> None:
    controller = TodolistWriteController(dependencies=sut)
    assert isinstance(controller, TodolistWriteController)