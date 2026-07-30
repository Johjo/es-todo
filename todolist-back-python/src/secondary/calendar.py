from datetime import date, datetime

from dependencies import Dependencies
from primary.controller.read.final_version_perfected import CalendarPort


class Calendar(CalendarPort):
    def today(self) -> date:
        return datetime.today().date()

    @classmethod
    def factory(cls, _: Dependencies) -> 'Calendar':
        return Calendar()
