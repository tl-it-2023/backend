from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from src.resume.router import router as router_resume

app = FastAPI()

api_router = APIRouter(
    prefix="/api"
)

api_router.include_router(
    router=router_resume
)

# Подключение всего
app.include_router(
    router=api_router
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)