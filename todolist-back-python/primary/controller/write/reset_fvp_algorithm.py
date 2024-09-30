from hexagon.fvp.write.reset_fvp_session import ResetFvpSession
from primary.controller.dependency_list import DependencyList


def reset_fvp_algorithm(dependencies: DependencyList):
    ResetFvpSession(dependencies.fvp_session_repository_for_fvp()).execute()
