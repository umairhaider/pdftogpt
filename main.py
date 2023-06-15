from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, upload_pdf, ask_question, get_presentation
from dotenv import load_dotenv
import os

# Load environment variables from .env file only in local development
if os.getenv("CI") is None:
    # Set the ENVIRONMENT variable to "development"
    os.environ["ENVIRONMENT"] = "development"
    load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(upload_pdf.router, prefix="/api/v1", tags=["Upload PDF"])
app.include_router(ask_question.router, prefix="/api/v1", tags=["Ask Question"])
app.include_router(get_presentation.router, prefix="/api/v1", tags=["Generate Presentation"])