import enum
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
    postgraduate_study = 1
    magistracy = 0.857
    specialty = 0.714
    bachelor_course = 0.571
    average = 0.428
    average_general = 0.285
    basic_general = 0.142
    none = 0


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
