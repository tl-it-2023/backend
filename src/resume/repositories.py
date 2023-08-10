from src.resume.models import ResumeFile, Resume


class ResumeFileRepository(SQLAlchemyRepository):
    model = ResumeFile


class ResumeRepository(SQLAlchemyRepository):
    model = Resume
