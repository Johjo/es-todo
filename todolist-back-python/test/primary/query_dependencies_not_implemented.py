from src.primary.port import QueryDependenciesPort
from src.primary.todolist.read.port import AllTaskPort


class QueryDependenciesNotImplemented(QueryDependenciesPort):
    def all_tasks(self) -> AllTaskPort:
        raise NotImplementedError()
