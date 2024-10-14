from collections import OrderedDict

from hexagon.fvp.domain_model import FvpSnapshot
from hexagon.fvp.port import FvpSessionSetPort


class ResetFvpSession:
    def __init__(self, set_of_fvp_sessions: FvpSessionSetPort):
        self.set_of_fvp_sessions : FvpSessionSetPort = set_of_fvp_sessions

    def execute(self):
        self.set_of_fvp_sessions.save(FvpSnapshot(OrderedDict()))
