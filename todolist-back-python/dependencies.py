from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any

class ResourceType(str, Enum):
    use_case = "use_case"
    adapter = "adapter"
    path = "path"
    infrastructure = "infrastructure"


@dataclass(frozen=True)
class Dependencies:
    factory: dict[Any, Any] = field(default_factory=dict)

    def feed(self, resource_type: ResourceType, resource: Any, factory: Any) -> 'Dependencies':
        return self._feed(resource_type=resource_type, resource=resource, factory=factory)

    def feed_use_case(self, use_case: Any, use_case_factory: Any) -> 'Dependencies':
        return self._feed(resource_type=ResourceType.use_case, resource=use_case, factory=use_case_factory)

    def feed_adapter(self, port: Any, adapter_factory: Any) -> 'Dependencies':
        return self._feed(resource_type=ResourceType.adapter, resource=port, factory=adapter_factory)

    def feed_path(self, path: str, factory) -> 'Dependencies':
        return self._feed(resource_type=ResourceType.path, resource=path, factory=factory)

    def feed_infrastructure(self, infrastructure: Any, factory):
        return self._feed(resource_type=ResourceType.infrastructure, resource=infrastructure, factory=factory)

    def _feed(self, resource_type: ResourceType, resource: Any, factory: Any) -> 'Dependencies':
        return replace(self, factory={**self.factory, (resource_type, resource): factory})

    def get_use_case(self, use_case: Any) -> Any:
        return self._get_resource(resource_type=ResourceType.use_case, resource=use_case)

    def get_query(self, query: Any) -> Any:
        return self.get_use_case(query)

    def get_infrastructure(self, infrastructure) -> Any:
        resource = self._get_resource(resource_type=ResourceType.infrastructure, resource=infrastructure)
        return resource

    def get_adapter(self, adapter: Any) -> Any:
        resource = self._get_resource(resource_type=ResourceType.adapter, resource=adapter)
        return resource

    def get_path(self, path_name: str) -> Any:
        return self._get_resource(resource_type=ResourceType.path, resource=path_name)



    def _get_resource(self, resource_type: ResourceType, resource) -> Any:
        assert (resource_type, resource) in self.factory, f"{resource_type.value} for {resource} must be injected first"
        return self.factory[(resource_type, resource)](self)

    @classmethod
    def create_empty(cls) -> 'Dependencies':
        return Dependencies()

