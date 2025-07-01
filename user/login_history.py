# login_history.py
# Tracks login/logout history for users in the Neyyal Billing System

from datetime import datetime
from typing import List
from utils.Tables import TableName as T
from utils.DB_conn import SessionLocal
from user.session import clear_current_session, set_current_session, get_current_user_name
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class LoginHistoryRecord(Base):
    """Represents a single login/logout record."""
    __tablename__ = T.LOGIN_HISTORY_TABLE.value  # Use the table name from the enum
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    login_time = Column(String, nullable=False)
    logout_time = Column(String, nullable=True)

    def as_list(self) -> List[str | int | None]:
        """Convert the record to a list for easy display."""
        return [
            getattr(self, "session_id", None),
            getattr(self, "username", None),
            getattr(self, "login_time", None),
            getattr(self, "logout_time", None)
        ]
    
class LoginHistory:
    """Handles login/logout history operations."""

    def __init__(self):
        """Initialize the LoginHistory class and create the login history table if it doesn't exist."""
        pass  # Table creation is handled in setup_db.py

    @staticmethod
    def record_login(username: str) -> int:
        """Record a user login event with the current timestamp and return the session_id."""
        login_time = datetime.now().isoformat(sep=' ', timespec='seconds')
        user = LoginHistoryRecord(username=username, login_time=login_time)
        with SessionLocal() as session:
            try:
                session.add(user)
                session.commit()
                return True
            except Exception:
                session.rollback()
                return False
        with SessionLocal() as session:
            # Retrieve the session_id for the newly created login event
            result = (
                session.query(LoginHistoryRecord.session_id)
                .filter(
                    LoginHistoryRecord.username == username,
                    LoginHistoryRecord.login_time == login_time
                )
                .order_by(LoginHistoryRecord.session_id.desc())
                .limit(1)
                .first()
            )
            if result and result[0]:
                session_id: int = result[0]
                set_current_session(username, session_id)
                return session_id
            else:
                raise ValueError("Failed to retrieve session_id for the login event.")

    @staticmethod
    def record_logout(session_id: int) -> None:
        """Record a user logout event with the current timestamp."""
        clear_current_session()  # Clear the current session_id
        logout_time = datetime.now().isoformat(sep=' ', timespec='seconds')
        with SessionLocal() as session:
            # Update the logout_time for the given session_id
            rowcount = session.query(LoginHistoryRecord).filter_by(session_id=session_id).update(
                {"logout_time": logout_time}
            )
            session.commit()
            if rowcount == 0:
                raise ValueError(f"Logout Failed! Failed for the User: {get_current_user_name()} (session_id={session_id})")

    def get_user_history(self, username: str) -> List[LoginHistoryRecord]:
        """Retrieve the login/logout history for a given user as a list of LoginHistoryRecord objects."""
        with SessionLocal() as session:
            return session.query(LoginHistoryRecord).filter_by(username=username).order_by(LoginHistoryRecord.session_id.desc()).all()

    def get_all_history(self) -> List[LoginHistoryRecord]:
        """Retrieve the complete login/logout history for all users as a list of LoginHistoryRecord objects."""
        with SessionLocal() as session:
            return session.query(LoginHistoryRecord).order_by(LoginHistoryRecord.session_id.desc()).all()

    def clear_history(self) -> None:
        """Clear the login/logout history table."""
        with SessionLocal() as session:
            session.execute(text(f'DELETE FROM {T.LOGIN_HISTORY_TABLE.value}'))
            session.commit()
        print("Login history cleared.")

    def get_login_history_as_list(self) -> List[List[str]]:
        """Get the login history as a list of lists for easy display."""
        history = self.get_all_history()
        return [[str(value) if value is not None else "" for value in record.as_list()] for record in history] if history else []