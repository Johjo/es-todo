from collections import OrderedDict

from src.dependencies import Dependencies
from src.hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort


class ResetFvpSession:
    def __init__(self, set_of_fvp_sessions: FvpSessionSetPort):
        self.set_of_fvp_sessions : FvpSessionSetPort = set_of_fvp_sessions

    def execute(self):
        self.set_of_fvp_sessions.save(FvpSnapshot(OrderedDict()))

    @classmethod
    def factory(cls, dependencies:Dependencies):
        return ResetFvpSession(dependencies.get_adapter(FvpSessionSetPort))