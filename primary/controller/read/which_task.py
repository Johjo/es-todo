from hexagon.fvp.read.which_task import WhichTaskQuery
from primary.controller.dependency_list import DependencyList


def which_task(name: str, dependencies: DependencyList):
    set_of_open_tasks = dependencies.task_reader_for_fvp_which_task(name)
    set_of_fvp_sessions = dependencies.fvp_session_repository_for_fvp()

    response = WhichTaskQuery(set_of_open_tasks=set_of_open_tasks, set_of_fvp_sessions=set_of_fvp_sessions).which_task()
    return response
