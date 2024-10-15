from collections import OrderedDict

from hexagon.fvp.aggregate import FvpSnapshot, FvpSessionSetPort


class ResetFvpSession:
    def __init__(self, set_of_fvp_sessions: FvpSessionSetPort):
        self.set_of_fvp_sessions : FvpSessionSetPort = set_of_fvp_sessions

    def execute(self):
        self.set_of_fvp_sessions.save(FvpSnapshot(OrderedDict()))
