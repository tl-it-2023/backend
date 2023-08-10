from src.resume.repositories import ResumeFileRepository, ResumeRepository
from src.resume.service import ResumeFileService, ResumeService


def resume_file_service():
    return ResumeFileService(ResumeFileRepository)


def resume_service():
    return ResumeService(ResumeRepository)
