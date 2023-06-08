from fastapi import APIRouter, UploadFile, File, HTTPException

from app.api import pdf_handler, question_handler

router = APIRouter()

@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    return await pdf_handler.upload_pdf(file)

@router.post("/ask_question/")
async def ask_question(question: str):
    return await question_handler.ask_question(question)