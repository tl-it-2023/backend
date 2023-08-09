from fastapi import APIRouter

router = APIRouter()


@router.get("/get_temp")
async def get_temp():
    return {"message": "Hello, World!"}
