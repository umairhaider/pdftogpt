import logging
import pdfplumber
from fastapi import HTTPException
from app.utils.langchain_utils import process_file_context, process_user_question

async def upload_pdf(file):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF file.")

    try:
        with pdfplumber.open(file.file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    logging.warning("A page could not be processed and was skipped.")

            process_file_context(text)
            return {"text": text, "generated_text": "The PDF file was successfully uploaded."}
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))