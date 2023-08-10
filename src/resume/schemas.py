import enum
from pydantic import BaseModel
from datetime import date


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


class ResumeSchema(BaseModel):
    id: int
    id_resume_file: int
    fio: str
    date_of_birth: date
    gender: Gender
    phone: str
    email: str


class ResumeSchemaAdd(BaseModel):
    fio: str
    date_of_birth: date
    gender: Gender
    phone: str
    email: str
