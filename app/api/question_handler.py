import logging
from fastapi import HTTPException
from app.utils.openai_utils import generate_chatgpt_response

async def ask_question(question):
    if not context:
        raise HTTPException(status_code=400, detail="Please upload a PDF file first.")

    # Create the prompt by combining the question and PDF context
    prompt = f"Question: {question}\nContext: {context}"

    try:
        generated_text = generate_chatgpt_response(prompt)
        return {"question": question, "answer": generated_text}
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))