from hexagon.fvp.aggregate import NothingToDo, DoTheTask, ChooseTheTask
from hexagon.fvp.read.which_task import TaskFilter, WhichTaskQuery
from dependencies import Dependencies


class FinalVersionPerfectedReadController:
    def __init__(self, dependencies: Dependencies):
        self._dependencies = dependencies

    def which_task(self, task_filter: TaskFilter) -> NothingToDo | DoTheTask | ChooseTheTask:
        query = self._dependencies.get_query(WhichTaskQuery)
        actual = query.which_task(task_filter)
        return actual
