import enum
from pydantic import BaseModel, Field
from datetime import datetime
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
    none = 3


class ResumeSchema(BaseModel):
    id: int
    id_resume_file: int
    fio: str
    date_of_birth: date
    gender: Gender
    phone: str
    email: str
      
    class Config:
        from_attributes = True


class ResumeSchemaAdd(BaseModel):
    id_resume_file: int
    fio: str
    date_of_birth: date
    gender: Gender
    phone: str
    email: str
