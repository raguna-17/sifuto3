from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.users.router import router as user_router
from app.organizations.router import router as organization_router
from app.job_applications.router import router as job_application_router


app = FastAPI()

origins = [os.getenv("FRONT", "http://localhost:5173")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(organization_router)
app.include_router(job_application_router)