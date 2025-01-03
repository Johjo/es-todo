from datetime import datetime

from src.dependencies import Dependencies
from src.primary.controller.write.todolist import DateTimeProviderPort


class DateTimeProvider(DateTimeProviderPort):
    def now(self) -> datetime:
        return datetime.now()

    @classmethod
    def factory(cls, _: Dependencies) -> 'DateTimeProvider':
        return DateTimeProvider()
