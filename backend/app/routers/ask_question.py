from fastapi import APIRouter, HTTPException, Depends
from app.models.user import User
from app.service import question_handler
from app.service.auth import get_current_user

router = APIRouter()

@router.post("/ask_question/")
async def ask_question(question: str, current_user: User = Depends(get_current_user)):
    """
    Ask a question and get a response based on the PDF context.

    Parameters:
    - question: The question to ask.

    Returns:
    - The response containing the generated answer.
    """
    # Ensure the user is authenticated
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return await question_handler.ask_question(question)