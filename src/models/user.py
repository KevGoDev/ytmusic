from typing import Optional

from sqlalchemy import Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, Session, mapped_column

from models import Base
from utils.user import hash_password


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column("username", String(64), nullable=False)
    email: Mapped[str] = mapped_column("email", String(128), nullable=False)
    password: Mapped[bytes] = mapped_column(
        "password", LargeBinary(128), nullable=False
    )

    @staticmethod
    def create(session: Session, username: str, email: str, password: str) -> "User":
        # Check if the username or email is already taken
        if User.get_by_username(session, username):
            raise Exception("Username is already taken")
        if User.get_by_email(session, email):
            raise Exception("Email is already taken")
        # Create user
        hashpw = hash_password(password)
        user = User(username=username, email=email, password=hashpw)
        session.add(user)
        session.flush()
        return user

    @staticmethod
    def get_by_id(session: Session, user_id: int) -> Optional["User"]:
        return session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_username(session: Session, username: str) -> Optional["User"]:
        return session.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_email(session: Session, email: str) -> Optional["User"]:
        return session.query(User).filter(User.email == email).first()

    def to_dict(self) -> dict:
        return {"id": self.id, "username": self.username, "email": self.email}
