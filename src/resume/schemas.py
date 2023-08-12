import enum

from fastapi import UploadFile
from pydantic import BaseModel
from datetime import date
from typing import List


class ResumeFileSchema(BaseModel):
    id: int
    file_name: str

    class Config:
        from_attributes = True


class ResumeFileSchemaAdd(BaseModel):
    file_name: str


class Gender(enum.Enum):
    man = 1
    woman = 2
    none = 3


class Education(enum.Enum):
    postgraduate_study = 'аспирантура'
    magistracy = 'магистратура'
    specialty = 'специалитет'
    higher = 'высшее'
    bachelor_course = 'бакалавриат'
    bachelor = 'бакалавр'
    average_first = 'среднее специальное'
    average_second = 'среднее профессиональное'
    average_general = 'среднее общее'
    basic_general = 'основное общее'
    none = ''


class ResumeSchema(BaseModel):
    id: int
    id_resume_file: int
    fio: str = None
    date_of_birth: date = None
    gender: Gender = None
    phone: str = None
    email: str = None
    education: Education = None
    experience: int = None
    profession: List[str] = None

    class Config:
        from_attributes = True


class ResumeSchemaAdd(BaseModel):
    id_resume_file: int
    fio: str = None
    date_of_birth: date = None
    gender: Gender = None
    phone: str = None
    email: str = None
    education: Education = None
    experience: int = None
    profession: List[str] = None
