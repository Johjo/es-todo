from abc import ABC, abstractmethod
from datetime import date

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import NothingToDo, DoTheTask, ChooseTheTask
from src.hexagon.fvp.read.which_task import WhichTaskQuery, WhichTaskFilter
from src.hexagon.shared.type import TodolistName


class FinalVersionPerfectedReadController:
    def __init__(self, dependencies: Dependencies):
        self._dependencies = dependencies

    def which_task(self, todolist_name: str, include_context: tuple[str, ...], exclude_context: tuple[str, ...], task_filter: WhichTaskFilter) -> NothingToDo | DoTheTask | ChooseTheTask:
        query : WhichTaskQuery = self._dependencies.get_query(WhichTaskQuery)
        calendar: CalendarPort = self._dependencies.get_adapter(CalendarPort)
        tf = WhichTaskFilter(todolist_name=TodolistName(todolist_name), include_context=include_context, exclude_context=exclude_context, reference_date=calendar.today())
        actual = query.which_task(tf)
        return actual


class CalendarPort(ABC):
    @abstractmethod
    def today(self) -> date:
        pass

