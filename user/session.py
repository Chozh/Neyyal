# session.py
# Module-level variables (global within this module)
current_user_name: str | None = None
current_session_id: int = 0

'''current user id and name for the session.
This module is used to store the current user's ID and name during the session.'''
def set_current_user(user_name: str) -> None:
    """Set the current user ID and name."""
    global current_user_name
    current_user_name = user_name

def clear_current_user() -> None:
    """Clear the current user ID and name."""
    global current_user_name
    current_user_name = None

def get_current_user_name() -> str | None:
    """Get the current user name."""
    return current_user_name

def set_current_session(user_name: str, session_id: int) -> None:
    """Set the current session."""
    global current_user_name
    current_user_name = user_name
    global current_session_id
    current_session_id = session_id

def get_current_session_id() -> int:
    """Get the current session ID."""
    return current_session_id

def clear_current_session() -> None:
    """Clear the current session ID."""
    global current_session_id, current_user_name
    current_session_id = 0
    current_user_name = None
