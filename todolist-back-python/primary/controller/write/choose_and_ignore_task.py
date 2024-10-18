from uuid import UUID

from hexagon.fvp.type import TaskKey
from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from primary.controller.dependency_list import DependencyList


def choose_and_ignore_task(chosen_task: UUID, ignored_task: UUID, dependencies: DependencyList) -> None:
    ChooseAndIgnoreTaskFvp(dependencies.fvp_session_repository_for_fvp()).execute(TaskKey(chosen_task), TaskKey(ignored_task))
