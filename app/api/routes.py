from fastapi import APIRouter, UploadFile, Form, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.models.user import User
from app.api import pdf_handler, question_handler
from app.service.auth import authenticate_user, create_access_token, get_current_user
from app.service.pptx_hander import generate_presentation

router = APIRouter()

@router.post("/signin/")
async def sign_in(username: str = Form(...), password: str = Form(...)):
    """
    Sign-in route for user authentication.

    Parameters:
    - username: The username for authentication.
    - password: The password for authentication.

    Returns:
    - A dictionary containing the access_token and token_type.
    """
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    """
    Upload a PDF file and process it.

    Parameters:
    - file: The UploadFile object representing the PDF file.

    Returns:
    - The response containing the processed data.
    """
    # Ensure the user is authenticated
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return await pdf_handler.upload_pdf(file)

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

@router.post("/get_presentation/")
async def get_presentation(current_user: User = Depends(get_current_user)):
    """
    Get a PPTX presentation based on the PDF context.

    Returns:
    - The response containing the generated answer.
    """
    # Ensure the user is authenticated
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    output_file = await generate_presentation()

    return StreamingResponse(open(output_file, "rb"),
                             media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                             headers={"Content-Disposition": "attachment; filename=presentation.pptx"})