from src.database import Base
from src.resume.schemas import ResumeFileSchema

from sqlalchemy.orm import (Mapped,
                            mapped_column)

from sqlalchemy import String


class ResumeFile(Base):
    __tablename__ = "resume_file"
    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String())

    def to_read_model(self) -> ResumeFileSchema:
        return ResumeFileSchema(
            id=self.id,
            file_path=self.file_name,
        )