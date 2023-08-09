from fastapi import FastAPI
from src.temp.router import router as router_temp

app = FastAPI()

app.include_router(
    router=router_temp,
    prefix="/temp"
)