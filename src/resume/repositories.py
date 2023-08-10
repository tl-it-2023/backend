from src.resume.models import ResumeFile, Resume
from src.utils import SQLAlchemyRepository


class ResumeFileRepository(SQLAlchemyRepository):
    model = ResumeFile


class ResumeRepository(SQLAlchemyRepository):
    model = Resume
