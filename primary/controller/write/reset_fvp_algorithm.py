from hexagon.fvp.write.reset_fvp_session import ResetFvpSession


def reset_fvp_algorithm():
    ResetFvpSession(set_of_fvp_session_repository).execute()
