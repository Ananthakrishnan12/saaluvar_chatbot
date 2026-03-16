from fastapi import FastAPI
from routers.appointment import router as appointment_router

app = FastAPI()

app.include_router(appointment_router)