import random
from typing import Annotated, List

from fastapi import APIRouter, UploadFile, Depends, Form, File
from fastapi.responses import JSONResponse
import os
from datetime import datetime

from src.resume.dependencies import resume_file_service, resume_service
from src.resume.service import ResumeFileService, ResumeService
from src.config import STORAGE_RESUME_FILE, STORAGE_RESUME
from src.resume.schemas import ResumeFileSchemaAdd, ResumeSchemaAdd, Education

from src.nlp.nlp import parse_resume

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


@router.get("/get_all_resume_files")
async def get_all(
        resume_file_service: Annotated[ResumeFileService, Depends(resume_file_service)],
):
    resume_files = await resume_file_service.get_resume_files()
    return resume_files


@router.post("/upload_resume_files")
async def upload_resume_files(
        resume_files: List[UploadFile],
        resume_file_service: Annotated[ResumeFileService, Depends(resume_file_service)],
        resume_service: Annotated[ResumeService, Depends(resume_service)]
):
    resumes = []
    c = 1
    for resume_file in resume_files:
        print(c)
        c += 1
        extension = resume_file.filename.split(".")[-1]
        file_name = f"resume_{datetime.now().strftime('%Y_%m_%d_%H-%M-%S-%f')}.{extension}"
        file_path = os.path.join(STORAGE_RESUME_FILE, file_name)
        resume_text = resume_file.file.read()
        with open(file_path, "wb") as file:
            file.write(resume_text)
        resume_file_id = await resume_file_service.add_resume_file(ResumeFileSchemaAdd(file_name=file_name))
        resume_value = parse_resume(resume_text.decode("utf-8"))
        resume_value.id_resume_file = resume_file_id
        resume = await upload_resume(resume_value, resume_service)
        resumes.append({"resume_file_id": resume_file_id, "resume": resume})
    return JSONResponse(content={"message": "Files uploaded successfully"}, status_code=200)


@router.post("/upload_resume_form")
async def upload_resume_form(
        fio: Annotated[str, Form()],
        phone: Annotated[str, Form()],
        email: Annotated[str, Form()],
        file: Annotated[UploadFile, File()],
        resume_file_service: Annotated[ResumeFileService, Depends(resume_file_service)],
        resume_service: Annotated[ResumeService, Depends(resume_service)]
):
    extension = file.filename.split(".")[-1]
    file_name = f"resume_{datetime.now().strftime('%Y_%m_%d_%H-%M-%S-%f')}.{extension}"
    file_path = os.path.join(STORAGE_RESUME_FILE, file_name)
    resume_text = file.file.read()
    with open(file_path, "wb") as resume:
        resume.write(resume_text)
    resume_file_id = await resume_file_service.add_resume_file(ResumeFileSchemaAdd(file_name=file_name))
    resume_value = parse_resume(resume_text.decode("utf-8"))
    resume_value.id_resume_file = resume_file_id
    if fio:
        resume_value.fio = fio
    if phone:
        resume_value.phone = phone
    if email:
        resume_value.email = email
    await upload_resume(resume_value, resume_service)
    return JSONResponse(content={"message": "Resume uploaded successfully"}, status_code=200)


@router.get("/test_parser")
async def test_parser(
        resume_file_service: Annotated[ResumeFileService, Depends(resume_file_service)]
) -> ResumeSchemaAdd:
    all_resume_files = await resume_file_service.get_resume_files()
    random_resume_file: ResumeFileService = random.choice(all_resume_files)
    with open(os.path.join(STORAGE_RESUME_FILE, random_resume_file.file_name), "r", encoding="utf-8") as resume_file:
        return parse_resume(resume_file.read())


@router.get("/get_all_resumes")
async def get_all_resume(
        resume_service: Annotated[ResumeService, Depends(resume_service)],
):
    resumes = await resume_service.get_resumes()
    return resumes


@router.get("/get_all_sorted_resumes")
async def get_all_sorted_resume(
        resume_service: Annotated[ResumeService, Depends(resume_service)],
):
    resumes = await resume_service.get_resumes()

    TYPES = {
        'аспирантура': 1,
        'магистратура': 0.857,
        'специалитет': 0.714,
        'высшее': 0.571,
        'бакалавриат': 0.571,
        'бакалавр': 0.571,
        'среднее специальное': 0.428,
        'среднее профессиональное': 0.428,
        'среднее общее': 0.285,
        'основное общее': 0.142
    }

    def schema_to_dict(r):
        return r.dict()

    resumes = list(map(schema_to_dict, resumes))

    for resume in resumes:
        try:
            value = resume.get('experience', 0) / 36 * 0.5 + TYPES.get(resume.get('education', 0).value) / TYPES.get(
                'среднее специальное') * 0.5
            resume['value'] = round(value, 2)
        except Exception as e:
            value = -1

    sorted_resumes = sorted(resumes, key=lambda resume: resume.get('value', 0), reverse=True)

    return sorted_resumes


@router.post("/upload_resume")
async def upload_resume(
        resume: ResumeSchemaAdd,
        resume_service: Annotated[ResumeService, Depends(resume_service)]
):
    resume_id = await resume_service.add_resume(resume)
    return {"resume_id": resume_id, "value": resume.model_dump()}
