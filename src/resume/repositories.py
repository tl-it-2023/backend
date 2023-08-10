from src.resume.models import ResumeFile
from src.utils import SQLAlchemyRepository


class ResumeFileRepository(SQLAlchemyRepository):
    model = ResumeFile