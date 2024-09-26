from test.hexagon.fvp.test_double import SimpleFvpSessionRepository

set_of_fvp_session_repository = SimpleFvpSessionRepository()

def init():
    global set_of_fvp_session_repository
    set_of_fvp_session_repository = SimpleFvpSessionRepository()
