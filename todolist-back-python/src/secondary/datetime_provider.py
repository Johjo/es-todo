from datetime import datetime

from dependencies import Dependencies
from primary.controller.write.todolist import DateTimeProviderPort


class DateTimeProvider(DateTimeProviderPort):
    def now(self) -> datetime:
        return datetime.now()

    @classmethod
    def factory(cls, _: Dependencies) -> 'DateTimeProvider':
        return DateTimeProvider()
