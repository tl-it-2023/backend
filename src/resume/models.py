from src.database import Base

from sqlalchemy.orm import (Mapped,
                            mapped_column)

from sqlalchemy import String


class ResumeFile(Base):
    __tablename__ = "resume_file"
    id: Mapped[int] = mapped_column(primary_key=True)
    temp: Mapped[str] = mapped_column(String())