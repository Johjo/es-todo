from collections import OrderedDict
from pathlib import Path
from uuid import UUID

from expression import Nothing

from dependencies import Dependencies
from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort
from hexagon.shared.type import TaskKey
from infra.json_file import JsonFile


class JsonSessionRepository(FvpSessionSetPort):
    def __init__(self, json_path: Path):
        self._json_file = JsonFile(json_path)

    def by(self) -> FvpSnapshot:
        d = self._json_file.read("all")
        if d == Nothing:
            return FvpSnapshot(OrderedDict[TaskKey, TaskKey]())
        return FvpSnapshot.from_primitive_dict({TaskKey(UUID(key)): TaskKey(UUID(value)) for (key, value) in d.value.items()})

    def save(self, snapshot: FvpSnapshot) -> None:
        self._json_file.insert("all", {str(key): str(value) for key, value in snapshot.to_primitive_dict().items()})

    @classmethod
    def factory(cls, dependencies: Dependencies) -> 'JsonSessionRepository':
        path = dependencies.get_path("session_fvp_json_path")
        return JsonSessionRepository(path)

