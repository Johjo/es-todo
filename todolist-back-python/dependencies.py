from abc import ABC
from dataclasses import dataclass, field, replace
from typing import Any


@dataclass(frozen=True)
class Dependencies(ABC):
    use_case_factory: dict[Any, Any] = field(default_factory=dict)
    adapter_factory: dict[Any, Any] = field(default_factory=dict)

    def feed_use_case(self, use_case: Any, use_case_factory: Any) -> 'Dependencies':
        return replace(self, use_case_factory={**self.use_case_factory, use_case: use_case_factory})

    def feed_adapter(self, port: Any, adapter_factory: Any) -> 'Dependencies':
        return replace(self, adapter_factory={**self.adapter_factory, port: adapter_factory})

    def get_use_case(self, use_case: Any) -> Any:
        assert use_case in self.use_case_factory, f"use_case for {use_case} must be injected first"
        return self.use_case_factory[use_case](self)

    def get_query(self, query: Any) -> Any:
        return self.get_use_case(query)

    def get_adapter(self, port) -> Any:
        assert port in self.adapter_factory, f"adapter for {port} must be injected first"
        return self.adapter_factory[port](self)

    @classmethod
    def create_empty(cls) -> 'Dependencies':
        return Dependencies()
