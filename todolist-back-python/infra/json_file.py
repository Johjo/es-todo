import json
from pathlib import Path
from typing import Any


class JsonFile:
    def __init__(self, path: Path):
        self._path = path

    def insert(self, key: str, value: Any) -> None:
        d = {**self._load_json(), key: value}
        self._path.write_text(json.dumps(d))

    def _load_json(self) -> dict:
        try:
            return json.loads(self._path.read_text())
        except FileNotFoundError:
            return {}

    def read(self, key: str) -> dict:
        values = self._load_json()
        return values[key]

    def all_keys(self) -> list[str]:
        values = self._load_json()
        return list(values.keys())
