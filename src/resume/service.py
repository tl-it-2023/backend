from src.resume.schemas import ResumeFileSchemaAdd
from src.utils import AbstractRepository


class ResumeFileService:
    def __init__(self, resume_file_repo: AbstractRepository):
        self.resume_file_repo: AbstractRepository = resume_file_repo()

    async def add_resume_file(self, resume_file: ResumeFileSchemaAdd):
        resume_file_dict = resume_file.model_dump()
        resume_file_id = await self.resume_file_repo.add_one(resume_file_dict)
        return resume_file_id

    async def get_resume_files(self):
        resume_files = await self.resume_file_repo.find_all()
        return resume_files