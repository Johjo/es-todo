from typing import NewType
from uuid import UUID

TaskKey = NewType('TaskKey', UUID)
TodolistName = NewType('TodolistName', str)
TodolistContext = NewType('TodolistContext', str)
TodolistContextCount = NewType('TodolistContextCount', int)