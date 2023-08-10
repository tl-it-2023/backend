import random
from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends
import os
from datetime import datetime

from src.resume.dependencies import resume_file_service, resume_service
from src.resume.service import ResumeFileService, ResumeService
from src.config import STORAGE_RESUME_FILE, STORAGE_RESUME
from src.resume.schemas import ResumeFileSchemaAdd, ResumeSchemaAdd

from src.nlp.nlp import parser_resume

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


@router.get("/get_all_file_names")
async def get_all(
        resume_file_service: Annotated[ResumeFileService, Depends(resume_file_service)],
):
    resume_files = await resume_file_service.get_resume_files()
    return resume_files


@router.post("/upload")
async def upload(
        resume_file: UploadFile,
        resume_file_service: Annotated[ResumeFileService, Depends(resume_file_service)]
):
    extension = resume_file.filename.split(".")[-1]
    file_name = f"resume_{datetime.now().strftime('%Y_%m_%d_%H-%M-%S-%f')}.{extension}"
    file_path = os.path.join(STORAGE_RESUME_FILE, file_name)
    with open(file_path, "wb") as file:
        file.write(resume_file.file.read())

    # TODO: добавляем nlp

    resume_file_id = await resume_file_service.add_resume_file(ResumeFileSchemaAdd(file_name=file_name))
    return {"resume_file_id": resume_file_id, "resume_file": resume_file}


@router.get("/test_parser")
async def test_parser(
        resume_file_service: Annotated[ResumeFileService, Depends(resume_file_service)]
):
    all_resume_files = await resume_file_service.get_resume_files()
    random_resume_file: ResumeFileService = random.choice(all_resume_files)
    with open(os.path.join(STORAGE_RESUME_FILE, random_resume_file.file_name), "r", encoding="utf-8") as resume_file:
        return parser_resume(resume_file.read())


@router.get("/test_get_all_resume")
async def test_get_all_resume(
        resume_service: Annotated[ResumeService, Depends(resume_service)],
):
    resumes = await resume_service.get_resumes()
    return resumes


@router.post("/test_upload_resume")
async def test_upload_resume(
        resume: ResumeSchemaAdd,
        resume_service: Annotated[ResumeService, Depends(resume_service)]
):
    resume_id = await resume_service.add_resume(resume)
    return {"resume_id": resume_id, "resume": resume}
