from src.resume.repositories import ResumeFileRepository
from src.resume.service import ResumeFileService


def resume_file_service():
    return ResumeFileService(ResumeFileRepository)
