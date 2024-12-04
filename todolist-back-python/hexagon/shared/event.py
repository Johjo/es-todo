from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True, eq=True)
class TaskPostponedEvent:
    task_key: UUID
    execution_date: date
