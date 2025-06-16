# session.py
current_user_id: int | None = None
current_user_name: str | None = None

'''current user id and name for the session.
This module is used to store the current user's ID and name during the session.'''
def set_current_user(user_id: int, user_name: str) -> None:
    """Set the current user ID and name."""
    global current_user_id, current_user_name
    current_user_id = user_id
    current_user_name = user_name

def get_current_user() -> tuple[int | None, str | None]:
    """Get the current user ID and name."""
    return current_user_id, current_user_name

def clear_current_user() -> None:
    """Clear the current user ID and name."""
    global current_user_id, current_user_name
    current_user_id = None
    current_user_name = None

def is_user_logged_in() -> bool:
    """Check if a user is logged in."""
    return current_user_id is not None and current_user_name is not None

def get_current_user_id() -> int | None:
    """Get the current user ID."""
    return current_user_id

def get_current_user_name() -> str | None:
    """Get the current user name."""
    return current_user_name
