import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, Session, mapped_column

from models import Base


class Download(Base):
    __tablename__ = "downloads"

    id: Mapped[int] = mapped_column(String(16), primary_key=True)
    title: Mapped[str] = mapped_column("title", String(256), nullable=False)
    path: Mapped[str] = mapped_column("path", String(512), nullable=False)
    status: Mapped[str] = mapped_column("status", String(256), nullable=True, default=None)
    progress: Mapped[float] = mapped_column("progress", Numeric(5, 2), nullable=True, default=0)
    created_at: Mapped[datetime.datetime] = mapped_column("created_at", DateTime, default=datetime.datetime.now)

    @staticmethod
    def create(
        session: Session,
        id: str,
        title: str,
        path: str,
    ) -> "Download":
        dl = Download(id=id, title=title, path=path)
        session.add(dl)
        session.flush()
        return dl

    @staticmethod
    def get_by_id(session: Session, video_id: str) -> Optional["Download"]:
        return session.query(Download).filter(Download.id == video_id).first()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "path": self.path,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at,
        }
