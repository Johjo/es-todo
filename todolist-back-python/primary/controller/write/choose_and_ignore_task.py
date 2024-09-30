from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from primary.controller.dependency_list import DependencyList


def choose_and_ignore_task(chosen_task, ignored_task, dependencies: DependencyList):
    ChooseAndIgnoreTaskFvp(dependencies.fvp_session_repository_for_fvp()).execute(int(chosen_task), int(ignored_task))
