from datetime import date

from primary.controller.read.todolist import CalendarPort


class _CalendarForTest(CalendarPort):
    def __init__(self) -> None:
        self._today: date | None = None

    def today(self) -> date:
        if self._today is None:
            raise Exception("feed today date")
        return self._today

    def feed_today(self, today):
        self._today = today

