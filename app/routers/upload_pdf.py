from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.models.user import User
from app.service.auth import get_current_user
from app.service import pdf_handler

router = APIRouter()

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