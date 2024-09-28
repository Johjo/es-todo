from primary.controller.dependency_list import DependencyList
from secondary.fvp.json_session_repository import JsonSessionRepository
from secondary.fvp.task_reader_todolist import TaskReaderTodolist
from secondary.todo_markdown_exporter.todo_reader_app import TodoReaderApp
from secondary.todo_markdown_importer.todo_writer_app import TodoWriterApp
from utils import SharedInstanceBuiltIn


class DependencyListWeb(DependencyList, SharedInstanceBuiltIn):
    def todo_writer_from_import_todolist_from_markdown(self, todolist_name):
        return TodoWriterApp(todolist_name=todolist_name)

    def task_reader_for_fvp_which_task(self, todolist_name):
        return TaskReaderTodolist(todolist_name=todolist_name)

    def fvp_session_repository_for_fvp(self):
        return JsonSessionRepository("session_fvp.json")

    def todo_reader_for_todo_markdown_exporter(self, name):
        return TodoReaderApp(name)
