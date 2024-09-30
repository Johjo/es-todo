from abc import ABC, abstractmethod


class DependencyList(ABC):
    @abstractmethod
    def todo_reader_for_todo_markdown_exporter(self, name):
        pass

    @abstractmethod
    def fvp_session_repository_for_fvp(self):
        pass

    @abstractmethod
    def task_reader_for_fvp_which_task(self, todolist_name: str, only_inbox: bool, context: str):
        pass

    @abstractmethod
    def todo_writer_from_import_todolist_from_markdown(self, todolist_name):
        pass
