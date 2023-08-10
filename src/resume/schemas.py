from pydantic import BaseModel


class ResumeFileSchema(BaseModel):
    id: int
    file_path: str

    class Config:
        from_attributes = True


class ResumeFileSchemaAdd(BaseModel):
    file_name: str
