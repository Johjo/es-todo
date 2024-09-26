from hexagon.fvp.write.choose_and_ignore_task import ChooseAndIgnoreTaskFvp
from toto import set_of_fvp_session_repository


def choose_and_ignore_task(chosen_task, ignored_task):
    ChooseAndIgnoreTaskFvp(set_of_fvp_session_repository).execute(int(chosen_task), int(ignored_task))
