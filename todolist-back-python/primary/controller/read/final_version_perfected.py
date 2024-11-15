from dependencies import Dependencies
from hexagon.fvp.aggregate import NothingToDo, DoTheTask, ChooseTheTask
from hexagon.fvp.read.which_task import WhichTaskQuery, WhichTaskFilter


class FinalVersionPerfectedReadController:
    def __init__(self, dependencies: Dependencies):
        self._dependencies = dependencies

    def which_task(self, task_filter: WhichTaskFilter) -> NothingToDo | DoTheTask | ChooseTheTask:
        query : WhichTaskQuery = self._dependencies.get_query(WhichTaskQuery)
        actual = query.which_task(task_filter)
        return actual
