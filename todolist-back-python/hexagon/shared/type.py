from typing import NewType
from uuid import UUID

TaskKey = NewType('TaskKey', UUID)
TaskName = NewType('TaskName', str)

TodolistName = NewType('TodolistName', str)
TodolistContext = NewType('TodolistContext', str)
TodolistContextCount = NewType('TodolistContextCount', int)