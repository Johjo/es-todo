from datetime import date
from typing import NewType
from uuid import UUID

TaskKey = NewType('TaskKey', UUID)
TaskName = NewType('TaskName', str)
TaskOpen = NewType('TaskOpen', bool)
TaskExecutionDate = NewType('TaskExecutionDate', date)

TodolistName = NewType('TodolistName', str)
TodolistContext = NewType('TodolistContext', str)
TodolistContextCount = NewType('TodolistContextCount', int)