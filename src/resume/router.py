from fastapi import APIRouter, UploadFile

router = APIRouter(
    prefix="/resume"
)


@router.post("/upload")
async def upload(file: UploadFile):
    print(file)
    return file