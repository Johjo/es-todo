import json
from collections import OrderedDict
from uuid import UUID

from hexagon.fvp.domain_model import FvpSnapshot
from hexagon.fvp.port import FvpSessionSetPort


class JsonSessionRepository(FvpSessionSetPort):
    def __init__(self, path: str):
        self.path = path

    def by(self) -> FvpSnapshot:
        try:
            with open(self.path, 'r') as file:
                json_content = json.loads(file.read())
                well_formated_data = {int(key): value for key, value in json_content.items()}
                return FvpSnapshot.from_primitive_dict(well_formated_data)
        except FileNotFoundError:
            return FvpSnapshot(OrderedDict[int, int]())

    def save(self, snapshot: FvpSnapshot) -> None:
        with open(self.path, 'w') as file:
            file.write(json.dumps(snapshot.to_primitive_dict(), indent=4))
