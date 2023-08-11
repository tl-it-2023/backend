from src.database import Base
from src.resume.schemas import ResumeFileSchema, ResumeSchema, Gender

from sqlalchemy.orm import (Mapped,
                            mapped_column)

from sqlalchemy import String, ForeignKey, Date, Enum
from datetime import date


class ResumeFile(Base):
    __tablename__ = "resume_file"
    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str] = mapped_column(String())

    def to_read_model(self) -> ResumeFileSchema:
        return ResumeFileSchema(
            id=self.id,
            file_name=self.file_name,
        )


class Resume(Base):
    __tablename__ = "resume"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_resume_file: Mapped[int] = mapped_column(ForeignKey("resume_file.id"), nullable=False)
    fio: Mapped[str] = mapped_column(String())
    date_of_birth: Mapped[date] = mapped_column(Date())
    gender: Mapped[Gender] = mapped_column(Enum(Gender))
    phone: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String())

    def to_read_model(self) -> ResumeSchema:
        return ResumeSchema(
            id=self.id,
            id_resume_file=self.id_resume_file,
            fio=self.fio,
            date_of_birth=self.date_of_birth,
            gender=self.gender,
            phone=self.phone,
            email=self.email,
        )
