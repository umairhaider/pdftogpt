import logging
from fastapi import HTTPException
from app.service.knowledgebase_handler import get_knowledge_base
from app.utils.langchain_utils import process_user_question


async def ask_question(user_question):
    knowledge_base = get_knowledge_base()
    if not knowledge_base:
        raise HTTPException(status_code=400, detail="Please upload a PDF file first.")
    
    try:
        generated_text = process_user_question(user_question)
        return {"question": user_question, "answer": generated_text}
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))