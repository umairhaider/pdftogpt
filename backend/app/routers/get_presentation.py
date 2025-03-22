from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.models.user import User
from app.service.auth import get_current_user
from app.service.pptx_hander import generate_presentation

router = APIRouter()

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