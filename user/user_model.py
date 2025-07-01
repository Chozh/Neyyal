# user_model.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from utils.DB_conn import engine, SessionLocal
from utils.Tables import TableName as T
from typing import Optional

Base = declarative_base()

class UserRecord(Base):
    __tablename__ = T.USERS_TABLE.value  # Use the table name from the enum
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    user_type = Column(String, nullable=False)
    added_by = Column(Integer, nullable=True)
    employee_id = Column(Integer, nullable=True)

    def as_list(self) -> list[int | str | None]:
        return [
            getattr(self, "user_id", None),
            getattr(self, "username", None),
            getattr(self, "password", None),
            getattr(self, "user_type", None),
            getattr(self, "added_by", None),
            getattr(self, "employee_id", None),
        ]

class UserModel:
    """Handles user-related database operations using SQLAlchemy ORM."""

    def __init__(self):
        Base.metadata.create_all(engine)

    def get_user_by_id(self, user_id: int) -> Optional[UserRecord]:
        with SessionLocal() as session:
            return session.query(UserRecord).filter_by(user_id=user_id).first()

    def get_user_by_username(self, username: str) -> Optional[UserRecord]:
        with SessionLocal() as session:
            return session.query(UserRecord).filter_by(username=username).first()

    def register_user(self, user: UserRecord) -> bool:
        with SessionLocal() as session:
            try:
                session.add(user)
                session.commit()
                return True
            except Exception:
                session.rollback()
                return False

    def user_exists(self, username: str) -> bool:
        with SessionLocal() as session:
            return session.query(UserRecord).filter_by(username=username).first() is not None
        
    def update_user(self, user_id: int, **kwargs: object) -> bool:
        with SessionLocal() as session:
            user = session.query(UserRecord).filter_by(user_id=user_id).first()
            if not user:
                return False
            for key, value in kwargs.items():
                setattr(user, key, value)
            try:
                session.commit()
                return True
            except Exception:
                session.rollback()
                return False
            
    def delete_user(self, user_id: int) -> bool:
        with SessionLocal() as session:
            user = session.query(UserRecord).filter_by(user_id=user_id).first()
            if not user:
                return False
            try:
                session.delete(user)
                session.commit()
                return True
            except Exception:
                session.rollback()
                return False

